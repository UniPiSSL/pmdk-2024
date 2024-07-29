#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

#define FILE_EXT ".sus"
#define FILE_PREFIX "ch4ll3ng_"
#define MAX_FILES 255

char* filenames[MAX_FILES];
size_t filenames_sz;

long generate_rng_seed()
{
	int fd = -1;
	long seed;

	fd = open(filenames[0], O_RDONLY);
	if(fd == -1)
	{	
		perror("Error opening file");
		exit(-1);
	}

	read(fd, &seed, 8);

	return seed;

}

void fetch_filenames(const char* prog_name)
{
    DIR *dir = opendir(".");

    if (dir == NULL) {
        perror("Error opening directory");
        exit(-1);
    }

    struct dirent *entry;
    size_t sz = 0;
    size_t filename_sz = 0;
    size_t prefix_len = strlen(FILE_PREFIX);

    while ((entry = readdir(dir)) != NULL && sz < MAX_FILES) {

    	if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0 || strcmp(entry->d_name, prog_name+2) == 0 || strncmp(entry->d_name, FILE_PREFIX, prefix_len) != 0)
    		continue;

    	filename_sz = strlen(entry->d_name) + 1;
    	char* filename = malloc(filename_sz);
    	strncpy(filename, entry->d_name, filename_sz);

    	filenames[sz++] = filename;

    }

    filenames_sz = sz;
    closedir(dir);
}

void clean_up()
{
	for(size_t i = 0; i < filenames_sz; i++)
	{
		free(filenames[i]);
		filenames[i] = NULL;
	}
}

size_t get_file_sz(const char *filename) {
    struct stat file_info;

    if (stat(filename, &file_info) == 0) {
        return file_info.st_size;
    } else {
        perror("stat");
        return -1;
    }
}

void enc_data(char* data, size_t sz)
{
	for(size_t i = 0; i < sz; i++)
	{
		data[i] ^= rand() % 256;
	}
}

char* append_ext(const char* filename)
{
	size_t file_sz = strlen(filename) + 1;

	char* new_filename = malloc(file_sz + sizeof(FILE_EXT));
	strncpy(new_filename, filename, file_sz);
	strcat(new_filename, FILE_EXT);

	return new_filename;
}

void create_enc_file(const char* filename, char* data, size_t sz, unsigned int id)
{
	int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
	if(fd == -1)
	{
		perror("open");
		exit(-1);
	}

	write(fd, &id, 4);
	write(fd, data, sz);
	close(fd);
}

void read_file(const char* filename, char* buf, size_t sz)
{
	int fd = open(filename, O_RDWR);
	read(fd, buf, sz);
	close(fd);
}

void enc_file(const char* filename, unsigned int id)
{
	size_t file_sz = get_file_sz(filename);

	char* buf = malloc(file_sz);
	
	read_file(filename, buf, file_sz);

	char* enc_filename = append_ext(filename);

	enc_data(buf, file_sz);

	create_enc_file(enc_filename, buf, file_sz, id);

	free(enc_filename);
	enc_filename = NULL;

	free(buf);
	buf = NULL;

}

int main(int argc, char* argv[])
{
	fetch_filenames(argv[0]);
	srand(generate_rng_seed());

	for(size_t i = 0; i < filenames_sz; i++)
	{
		enc_file(filenames[i], i);
	}

	clean_up();

	return 0;
}
