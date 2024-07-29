#!/usr/bin/env ruby
require 'sinatra'
require 'open-uri'
require 'nokogiri'
require 'net/http'

get '/' do
	erb :index
end

before '/flag' do
	puts "request.ip = #{request.ip}"
	halt 403, "Forbidden - Access allowed only from localhost" unless is_localhost_ip?(request.ip)
end

post '/search' do
	@url = params[:url]
	@search_string = params[:search_string]

	if is_localhost_url?(@url)
		halt 403, "This URL can not be searched."
	elsif @url && @search_string
		@result = search_website(@url, @search_string)
	else
		halt 500, "Invalid search query."
	end

	erb :result
end

get '/flag' do
	@result = File.read('flag.txt').strip rescue 'CTFLIB{example-flag}'
	erb :result
end

error 403 do
	@error_type = "warning"
	@error_message = body[0]
	erb :error
end

error 500 do
	@error_type = "danger"
	@error_message = body[0]
	erb :error
end

def is_localhost_url?(url)
	uri = URI.parse(url)
	host_ip = IPSocket.getaddress(uri.host)
	is_localhost_ip?(host_ip)
rescue SocketError
	false
end

def is_localhost_ip?(ip)
	localhost_addresses = ['0.0.0.0', '127.0.0.1', '::1', '::ffff:127.0.0.1']
	localhost_addresses.include?(ip)
end

def load_website(url, redirect_limit = 5)
	raise "Exceeded redirect limit" if redirect_limit <= 0

	uri = URI.parse(url)

	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = (uri.scheme == 'https')
	http.verify_mode = OpenSSL::SSL::VERIFY_NONE

	request = Net::HTTP::Get.new(uri.path)
	response = http.request(request)

	case response
	when Net::HTTPSuccess
		response.body
	when Net::HTTPRedirection
		new_location = response['location']
		new_uri = URI.parse(new_location)
		
		# Check if the new location is an absolute URL or a relative path
		if new_uri.host.nil?
			# If it's a relative path, construct the full URL
			new_uri = URI.join(url, new_location)
		end
		
		load_website(new_uri.to_s, redirect_limit - 1)
	else
		raise "Error loading the URL: #{response.code} - #{response.message}"
	end
end

def search_website(url, search_string)
	begin
		html = load_website(url)
		doc = Nokogiri::HTML(html)

		doc.xpath('//head').remove
		doc.xpath('//script').remove
		doc.xpath('//style').remove

		text = doc.text
		find_text_with_context(text, search_string)
	rescue StandardError => e
		halt 500, "An error occurred: #{e.message}"
	end
end

def find_text_with_context(text, search_string, len = 250)
	found_text = []
	len = (len - search_string.length) / 2
	text.scan(/(\S*.{0,#{len}}#{Regexp.escape(search_string)}.{0,#{len}}\S*)/i) do |match|
		found_text << match[0].strip
	end
	found_text.sort_by { |item| item.length }.reverse
end
