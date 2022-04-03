# Creating a function that generates a customized questionnaire in PDF
# The QR Code is the tool for customisation

# The function is named custom_question
def custom_question(px_code):
    import os.path

    import qrcode
    from pylatex import Document, Section, Head, LargeText, MiniPage, StandAloneGraphic, \
        NewLine, Tabularx, Tabu, Command, MediumText
    from pylatex import Package
    from pylatex.utils import bold, NoEscape

    # ...
# The layout specifications
    geometry_options = {"margin": "0.5in",
                        "head": "2cm",
                        "headsep": "10pt",
                        "bottom": "0.6in",
                        "top": "1.0cm",
                        "rmargin": "4cm",
                        "tmargin": "0.5cm",
                        "lmargin": "0.8cm",
                        "inputenc": "utf8"
                        }

# QRCode specifications
    makebarcode_options = {"code": "Code39", "X": ".5mm", "ratio": ".25", "H": "1cm"}
    doc = Document(geometry_options=geometry_options,
                   document_options=["a4paper", "24pt"], fontenc='Helvet', page_numbers=None)
# Generating the QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=200,
        border=0.1,
    )
    qr.add_data(px_code, )
    qr.make(fit=True)
# Importing the logo to be used on the project
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qr_img.png')

    two = NoEscape(r'\bigcirc')

# Now to the main document - adding all the images, QRCode and positioning them
    with doc.create(Head()) as header_right:
        with header_right.create(MiniPage(width=NoEscape(r"0.9\textwidth"),
                                          pos='l', fontsize="Large")) as logo_wrapper:
            logo_file = os.path.join(os.path.dirname(__file__), 'logo.jpeg')
            logo_wrapper.append(StandAloneGraphic(image_options="width = 150px", filename=logo_file))
            logo_wrapper.append(NewLine(LargeText(bold("PATIENTS EXPERIENCE SURVEY"))))

    with doc.create(Head()) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"), pos='R')) as left_wrapper:
            left_wrapper.append(StandAloneGraphic('qr_img.png', "width = 80px"))

# Adding the 1st section - The instruction
    with doc.create(Section("", label=False, numbering=False)):
        doc.append(MediumText
                   ('We would like to ask you some questions about your recent stay in Garki Hospital Abuja.'))
        doc.append('\n')
        doc.append(MediumText('Your response will help us to improve the quality of our hospital services.'))
        doc.append('\n')
        doc.append(MediumText('All your answers are strictly confidential.'))
        doc.append('\n')
        doc.append(MediumText(bold("Please assess us by shading the box that best represent your experience.")))
        doc.append('\n')
        doc.append(MediumText('Thank you'))
        doc.append('\n')
        doc.append('\n')

    doc.packages.append(Package("fontspec,xunicode,array"))

# Table for the second section
    with doc.create(Tabularx("X[r], X[r], X[r], X[r], X[r], X[r]",
                             row_height=2, width_argument=NoEscape(r'1.5\textwidth'))) as table:
        header_row = ["Question", "Very Poor", "Poor", "Fair", "Good", "Excellent"]

        table.add_hline()
        table.add_row(header_row, mapper=[bold])
        table.add_hline()
        table.add_row(MediumText("The ward (or room) I stayed in was clean"), two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("The nurses responded to my (or my patient’s) needs effectively"), \
                      two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("The nurses knew enough about my (or my patient’s) condition and treatment"), \
                      two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("The nurses discussed my (or my patient’s) condition and treatment \
        with me in a way I could understand"), two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("The nurses responded to my (or my patient’s) requests in a reasonable time"), \
                      two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("I (or my patient) was kept as physically comfortable as I could hope to be"), \
                      two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("I (or my patient) got emotional support from the nurses during my stay"), \
                      two, two, two, two, two)
        # table.add_hline()
        table.add_row(MediumText("Do you have any comment?:"), "", "", "", "", "")
        doc.append('\n')
        table.add_row("", "", "", "", "", "")
        table.add_hline()
        table.add_row("", "", "", "", "", "")
        table.add_hline()
        table.add_row("", "", "", "", "", "")
        table.add_hline()

    doc.append('\n')
    doc.append('\n')

# Section for the biodata
    with doc.create(Tabu("X[l], X[r], X[c], X[l]", col_space="0.2in", booktabs=False)) as age:
        age.add_row(MediumText("I am..."), MediumText("Male"), MediumText("Female"), " ")
        age.add_row(MediumText(" "), MediumText(two), MediumText(two), MediumText(" "))
        age.add_row("", "", "", "")
        age.add_row(MediumText("My age is..."), MediumText("18 - 35years"), MediumText("36 - 49years"),
                    MediumText("50years & above"))
        age.add_row(" ", two, two, two)

    with doc.create(MiniPage(width=NoEscape(r'1\textwidth'))) as bio:
        bio.append(NoEscape(r'\bigcirc' "Male"))

    doc.generate_pdf("test", clean=True, compiler="xelatex")

    return(custom_question())

# Creating a datetime element which is part of the make up of the QRCode
from datetime import date
today = date.today()
day = today.strftime("%d%m%Y")
def ucode(ward, cubicle):
    c = day + ward + cubicle
    return c


