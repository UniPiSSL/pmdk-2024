#!/usr/bin/env python3
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# Load flag
flag = b'FLAG{this-is-an-example-flag}'
if os.path.exists('flag.txt'):
    flag = open('flag.txt', 'r').read().strip().encode()
else:
    print('WARNING! Using example flag.')


A4_W, A4_H = A4

def AllPageSetup(canvas, doc):
	canvas.saveState()

	# Set black bg
	canvas.setFillColor(HexColor("#000000"))
	path = canvas.beginPath()
	path.moveTo(0, 0)
	path.lineTo(0, A4_H)
	path.lineTo(A4_W, A4_H)
	path.lineTo(A4_W, 0)
	canvas.drawPath(path, True, True)

	canvas.restoreState()


# Create a PDF document with black background
pdf = SimpleDocTemplate("flag.pdf", pagesize=A4)

# Define styles for white text on black background
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
	name='Normal_JUSTIFY',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_JUSTIFY,
	fontSize=12,
	leading=13,
	textColor=colors.white,
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Small_JUSTIFY',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_JUSTIFY,
	fontSize=10,
	leading=11,
	textColor=colors.white,
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Normal_CENTER_purple',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_CENTER,
	fontSize=14,
	leading=15,
	textColor=HexColor("#9900ff"),
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Normal_CENTER_red',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_CENTER,
	fontSize=14,
	leading=15,
	textColor=HexColor("#ff0000"),
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Big_CENTER',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_CENTER,
	fontSize=18,
	leading=19,
	textColor=colors.white,
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Big_CENTER_Blue',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_CENTER,
	fontSize=18,
	leading=19,
	textColor=HexColor("#03a9f4"),
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Small_CENTER_Blue',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_CENTER,
	fontSize=12,
	leading=13,
	textColor=HexColor("#03a9f4"),
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))
styles.add(ParagraphStyle(
	name='Very_Small_CENTER',
	parent=styles['Normal'],
	fontName='Helvetica',
	wordWrap='LTR',
	alignment=TA_CENTER,
	fontSize=8,
	leading=9,
	textColor=colors.white,
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True
))



#black_background_style = ParagraphStyle('black_background', parent=styles['BodyText'], textColor=colors.white, backColor=colors.black)

# Content for each page
content = []

# Page 1
content.append(Spacer(width=0, height=(A4_H/3)))
content.append(
	Paragraph(
		"Before you read this document, please have this playing in the background:",
		styles['Big_CENTER']
	)
)

content.append(Spacer(width=0, height=22))
link = 'https://youtu.be/RaQGqjYcxAg'
content.append(
	Paragraph(
		f"<link href=\"{link}\">{link}</link>",
		styles['Big_CENTER_Blue']
	)
)
content.append(PageBreak())


# Page 2
content.append(Spacer(width=0, height=(3*A4_H/7)))
content.append(
	Paragraph(
		"I am serious, go do it, open the link.",
		styles['Big_CENTER']
	)
)
content.append(PageBreak())


# Page 3
content.append(Spacer(width=0, height=(3*A4_H/7)))
content.append(
	Paragraph(
		"Alright I hope you’re ready :D",
		styles['Big_CENTER']
	)
)
content.append(PageBreak())


# Page 4
content.append(
	Paragraph(
		"As the pentester got out his laptop and began dissecting the code he asked the challenge:",
		styles['Normal_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=22))
content.append(
	Paragraph(
		str("“Are you difficult to solve because your cursed technique is RSA?\nOr is your cursed technique RSA because you’re difficult to solve?”").replace('\n','<br />\n'),
		styles['Normal_CENTER_purple']
	)
)
content.append(Spacer(width=0, height=50))
img = Image('image-1.jpg')
img.drawHeight = img.drawHeight / 2
img.drawWidth = img.drawWidth / 2
content.append(img)
content.append(PageBreak())


# Page 5
content.append(
	Paragraph(
		"The challenge then replied:",
		styles['Normal_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=22))
content.append(
	Paragraph(
		str("“Stand proud, you are strong. But you’re a fool for thinking you can\nbeat the king of curses. <b>Arm yourself</b>.”").replace('\n','<br />\n'),
		styles['Normal_CENTER_red']
	)
)
content.append(Spacer(width=0, height=50))
img = Image('image-2.jpg')
img.drawHeight = img.drawHeight * 0.35
img.drawWidth = img.drawWidth * 0.35
content.append(img)


content.append(Spacer(width=0, height=50))
content.append(
	Paragraph(
		"For unbeknownst to the pentester, the challenge had transformed the plaintext by passing it into an obscure polynomial function before performing multiple RSA encryptions on it.",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))
content.append(
	Paragraph(
		"In that moment, the challenge could’ve saved itself, but it did not know 2 key things:",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))
content.append(
	Paragraph(
		'<br />'.join([
			'&nbsp;&nbsp;&nbsp; • The first is to always bet on the pentester.',
			'&nbsp;&nbsp;&nbsp; • The second is that the pentester knew Chinese Remainder Theorem.'
		]),
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))

content.append(
	Paragraph(
		"The pentester combined his techniques:",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))

content.append(
	Paragraph(
		'<br />'.join([
			'&nbsp;&nbsp;&nbsp; • Chinese Remainder Theorem - To recover the output of the obscure function',
			'&nbsp;&nbsp;&nbsp; • Sympy - To parse the 4th degree polynomial into Python (or not hehehe)',
			'&nbsp;&nbsp;&nbsp; • Equation Solving - To construct f(x) = f(AES_KEY) and solve for x (the key)'
		]),
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))

content.append(
	Paragraph(
		"And then, he unleashed a force that all men should fear:",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))

content.append(
	Paragraph(
		"Domain Expansion: Asymmetry",
		styles['Normal_CENTER_purple']
	)
)
content.append(Spacer(width=0, height=12))

content.append(
	Paragraph(
		"The pentester’s domain: Asymmetry. It is an exceptionally refined domain that undermines symmetric ciphers. In a battle where the opponent’s domain is AES based, Asymmetry is sure to overtake it. The adversary has absolutely no chance of victory.",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=12))

content.append(PageBreak())




# Page 6
content.append(
	Paragraph(
		"In a battle of domains, cursed techniques are rendered practically useless, hence why Asymmetry is such a powerful trump card in this case.",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=22))

content.append(
	Paragraph(
		"The challenge’s cursed technique “Repeated RSA”, which is an asymmetric cipher, is irrelevant. When both parties expand their domains, the battle will ONLY be decided according to whose domain is stronger. If the challenge’s domain was an asymmetric cipher, the battle would be much closer in terms of power.",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=22))

content.append(
	Paragraph(
		"In addition, inside your own domain, your attacks are guaranteed to hit the opponent within a predetermined radius (100 meters). The challenge could no longer escape.",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=22))

content.append(
	Paragraph(
		"The pentester, knowing that his Domain is far superior to that of the challenge’s, stood proud, and arrogantly struck his final pose:",
		styles['Small_JUSTIFY']
	)
)
content.append(Spacer(width=0, height=22))

img = Image('image-3.jpg')
img.drawHeight = img.drawHeight * 0.45
img.drawWidth = img.drawWidth * 0.45
content.append(img)
content.append(Spacer(width=0, height=22))

content.append(
	Paragraph(
		flag,
		styles['Small_CENTER_Blue']
	)
)
content.append(Spacer(width=0, height=22))

link = 'https://youtu.be/jPZlabsAlVM'
content.append(
	Paragraph(
		str(f"Bonus:\n<link href=\"{link}\">{link}</link>").replace('\n','<br />\n'),
		styles['Very_Small_CENTER']
	)
)




'''
content.append(Paragraph("This is the introduction paragraph.", styles['BodyText']))
content.append(Image('image-1.jpg', width=400, height=300))

# Page 2
content.append(Paragraph("Page 2 - Main Content", black_background_style))
content.append(Paragraph("This is the main content paragraph.", styles['BodyText']))
content.append(Image('image-1.jpg', width=400, height=300))

# Page 3
content.append(Paragraph("Page 3 - Additional Information", black_background_style))
content.append(Paragraph("This is some additional information.", styles['BodyText']))
content.append(Image('image-1.jpg', width=400, height=300))

# Page 4
content.append(Paragraph("Page 4 - Conclusion", black_background_style))
content.append(Paragraph("This is the conclusion paragraph.", styles['BodyText']))
content.append(Image('image-1.jpg', width=400, height=300))
'''

# Build the PDF document
pdf.build(content, onFirstPage=AllPageSetup, onLaterPages=AllPageSetup)


