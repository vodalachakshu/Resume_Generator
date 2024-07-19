import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
import io

def create_pdf(name, email, phone, address, summary, experience, education, skills):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Draw header background
    header_height = 120
    c.setFillColor(colors.HexColor("#4F81BD"))
    c.rect(0, height - header_height, width, 100, fill=1)
    
    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, height - 50, name)
    
    # Contact Information
    c.setFont("Helvetica", 12)
    contact_y_start = height - header_height + 45
    c.drawString(72, contact_y_start, email)
    c.drawString(72, contact_y_start - 16, phone)
    c.drawString(72, contact_y_start - 32, address)
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header', fontSize=16, leading=16, spaceAfter=10, textColor=colors.HexColor("#4F81BD")))
    styles.add(ParagraphStyle(name='Content', fontSize=12, leading=14, spaceAfter=10))
    
    # Create a Frame for the content
    frame = Frame(72, 72, width - 144, height - 216, showBoundary=0)
    
    elements = []
    
    # Summary
    elements.append(Paragraph("<b>Summary</b>", styles['Header']))
    elements.append(Paragraph(summary, styles['Content']))
    
    # Experience
    elements.append(Paragraph("<b>Experience</b>", styles['Header']))
    
    experience_data = [['Position', 'Company', 'Duration', 'Description']]
    experience_lines = experience.split('\n')
    for line in experience_lines:
        if line.strip():
            parts = line.split('|')
            if len(parts) == 4:
                experience_data.append(parts)
    
    experience_table = Table(experience_data, colWidths=[100, 100, 100, 200])
    experience_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(experience_table)
    
    # Education
    elements.append(Paragraph("<b>Education</b>", styles['Header']))
    
    education_data = [['Degree', 'Institution', 'Year', 'Details']]
    education_lines = education.split('\n')
    for line in education_lines:
        if line.strip():
            parts = line.split('|')
            if len(parts) == 4:
                education_data.append(parts)
    
    education_table = Table(education_data, colWidths=[100, 100, 100, 200])
    education_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(education_table)
    
    # Skills
    elements.append(Paragraph("<b>Skills</b>", styles['Header']))
    elements.append(Paragraph(skills, styles['Content']))
    
    # Build the PDF
    frame.addFromList(elements, c)
    
    c.save()
    buffer.seek(0)
    return buffer

def main():
    st.title("Resume Builder")

    st.header("Personal Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")

    st.header("Professional Summary")
    summary = st.text_area("Summary")

    st.header("Work Experience")
    st.write("Enter each experience on a new line in the format: Position | Company | Duration | Description")
    experience = st.text_area("Experience")

    st.header("Education")
    st.write("Enter each education detail on a new line in the format: Degree | Institution | Year | Details")
    education = st.text_area("Education")

    st.header("Skills")
    skills = st.text_area("Skills")

    if st.button("Generate PDF"):
        pdf = create_pdf(name, email, phone, address, summary, experience, education, skills)
        st.download_button("Download PDF", data=pdf, file_name="resume.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()

