#!/usr/bin/env python3
#MIT License
#
#Copyright (c) 2024 Hackacharya
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
# 
# ---------------------------------------------------------------------


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame



import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from typing import List, Dict
from collections import defaultdict
import markdown
import csv
import pandas as pd
from io import StringIO

# Tobedone
class HeaderFooterDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, header_str, footer_str, **kwargs):
        super().__init__(filename, **kwargs)
        self.footer_text = footer_str
        self.hdr_text = header_str
        self.addPageTemplates(PageTemplate(id='normal', frames=[Frame(0, 0, 6*inch, 9*inch)]))

    def onLaterPages(self, canvas, doc):
        print('on later canvas called')
        canvas.saveState()
        canvas.setFillColor('black')
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(1 * inch, 0.75 * inch, self.footer_text)
        canvas.restoreState()

    def footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, self.footer_text) 
        canvas.restoreState()

def read_csv(file_path: str) -> List[Dict[str, str]]:
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        for row in reader:
            summary = row['Summary']
            #print(f'read summary -> {summary}', flush=True) 
            row['Priority'] = 99999;
            if row.get('Priority'):
                try:
                    row['Priority'] = int(row['Priority'])
                except ValueError:
                    pass; 
            # Split Labels by commas or semicolons if present
            if row.get('Labels'):
                row['Labels'] = [label.strip() for label in row['Labels'].split(',')]
            data.append(row)
    return data

def group_by_category(data: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    grouped_data = defaultdict(list)
    for row in data:
        category = row.get('Category', 'Uncategorized')
        grouped_data[category].append(row)
    
    # Sort items within each category by Priority (ascending)
    for category, items in grouped_data.items():
        grouped_data[category] = sorted(items, key=lambda x: x.get('Priority', float('inf')))
    
    return grouped_data

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_revision_history(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Convert Markdown table to DataFrame
    html_content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    df = pd.read_html(StringIO(html_content))[0]
    return df

def generate_markdown(grouped_data: Dict[str, List[Dict[str, str]]], output_file: str, title_content: str = "", bg_content: str = "", appendix_content: str = "", revision_history: str = ""):
    with open(output_file, 'w', encoding='utf-8') as file:
        if title_content:
            file.write(f'# {title_content}\n\n')
        if bg_content:
            file.write(f'## Background and Introduction\n\n{bg_content}\n\n')
        
        for category, items in grouped_data.items():
            file.write(f'\n\n## {category}\n\n')
            for item in items:
                summary = item.get('Summary', '')
                description = item.get('Description', '').strip()
                labels = item.get('Labels', [])
                priority = item.get('Priority', '')

                # Ensure labels is always a list
                if not isinstance(labels, list):
                    labels = []
                
                labels_str = ', '.join(labels)  # Join labels with a comma

                file.write(f'- [ ] {summary}\n')
                
                if len(description) > 0:
                    file.write(f'  {description}\n\n') 
                
                """
                don't need this.
                metadata = "";
                if priority:
                   metadata = f'P{priority}, '
                if labels_str:
                   metadata = metadata + f'{labels_str}'
                file.write(f'  *{metadata}*\n')
                file.write('\n')
                """
        
        if appendix_content:
            file.write('\n## Appendix\n\n')
            file.write(appendix_content)
        
        if revision_history:
            file.write('\n## Revision History\n\n')
            file.write(revision_history)



def generate_pdf(grouped_data: Dict[str, List[Dict[str, str]]], output_file: str, title_content: str = "", bg_content: str = "", appendix_content: str = "", revision_history_df: pd.DataFrame = None, footer_text: str = ""):
    doc = HeaderFooterDocTemplate(output_file, header_str='', footer_str=footer_text, pagesize=letter)
    #doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Title page styles
    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=30,
        alignment=2,  # Center align
        spaceAfter=100,  # Space after the title
        leading=30,  # Leading to avoid overlap
    )
    
    normal_style = styles["Normal"]
    header_style = styles['Heading1']
    content_style = styles['BodyText']
    italic_style = ParagraphStyle(
        name='ItalicStyle',
        fontSize=12,
        alignment=0,
        fontName='Helvetica-Oblique',
        leftIndent=20
    )
    checklist_style = ParagraphStyle(
        name='ChecklistStyle',
        fontSize=12,
        alignment=0,
        leftIndent=20,
        leading=20,
	    fontName='Courier',
    )

    symbol_style = ParagraphStyle(
        'SymbolStyle',
        checklist_style.parent,
        fontsize=20,
        leading=0,
        spaceBefore=0,
        spaceAfter=0,
    )

    description_style = ParagraphStyle(
        name='DescriptionStyle',
        fontSize=12,
        alignment=0,
        leftIndent=40,  # Indent for description
        spaceAfter=6  # Space after description
    )
    footer_style = ParagraphStyle(
        name='FooterStyle',
        fontSize=10,
        alignment=2,
        spaceBefore=12,
        spaceAfter=12,
        fontName='Helvetica-Oblique',
    )
    appendix_style = ParagraphStyle(
        name='AppendixStyle',
        fontSize=12,
        alignment=0,
        spaceBefore=12
    )
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d5d5d5'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    
    pdfelems = []

    if title_content:
        pdfelems.append(Paragraph(title_content.replace('\n', '<br />'), title_style))
        pdfelems.append(PageBreak())  # Page break after title page

    if bg_content:
        pdfelems.append(Paragraph('Background and Introduction', header_style))
        pdfelems.append(Spacer(1, 12))
        pdfelems.append(Paragraph(bg_content.replace('\n', '<br />'), content_style))
        pdfelems.append(PageBreak())  # Page break after introduction

    for category, items in grouped_data.items():
        if not category:
            category = "None";

        pdfelems.append(Paragraph('<br/>'+category, header_style))
        pdfelems.append(Spacer(1, 12))
        for item in items:
            summary = item.get('Summary', '')
            description = item.get('Description', '').strip()
            labels = item.get('Labels', [])
            priority = item.get('Priority', '')
            
            if not isinstance(labels, list):
                labels = []
                
            labels_str = ', '.join(labels)
            
            pdfelems.append(Paragraph('&#9745 ', symbol_style))
            pdfelems.append(Paragraph(f'{summary}', checklist_style))
            
            if len(description) > 0:
                description_paragraph = Paragraph(description.replace('\n', '<br />'), description_style)
                pdfelems.append(description_paragraph)

            """ 
            Don't need this.
            metadata = "";
            if priority:
                metadata = f'P{priority}, '
            if labels_str:
                metadata = metadata + f'{labels_str}'
            pdfelems.append(Paragraph(metadata, italic_style))
            """
            pdfelems.append(Spacer(1, 6))
    
    if appendix_content:
        pdfelems.append(PageBreak())
        pdfelems.append(Paragraph('Appendix', header_style))
        pdfelems.append(Spacer(1, 12))
        pdfelems.append(Paragraph(appendix_content.replace('\n', '<br />'), appendix_style))
    
    if revision_history_df is not None:
        pdfelems.append(PageBreak())
        pdfelems.append(Paragraph('Revision History', header_style))
        pdfelems.append(Spacer(1, 12))
        
        # Generate data from table , take care of line wraps for a decent looking rev history
        data = [revision_history_df.columns.tolist()];
        for row in revision_history_df.values.tolist():
            wrapped_row = [Paragraph(str(val), normal_style) for val in row]
            data.append(wrapped_row)
        table = Table(data, colWidths=[40,80,200,100])
        table.setStyle(table_style)
        pdfelems.append(table)

    # Ugly this comes at the very end - how to add footer 
    if footer_text and len(footer_text)> 0:
        #pdfelems.append(PageBreak())  # Optional: Page break before footer
        pdfelems.append(Paragraph(footer_text, footer_style))
    
    doc.build(pdfelems)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Markdown or PDF from JIRA CSV import template.')
    parser.add_argument('csv_file', help='Path to the JIRA CSV import file.')
    parser.add_argument('output_file', help='Path to the output Markdown or PDF file.')
    parser.add_argument('--format', choices=['markdown', 'pdf'], default='markdown', help='Output format.')
    parser.add_argument('--title', help='Path to the title page content text file.')
    parser.add_argument('--background', help='Path to the Background and Introduction content text file.')
    parser.add_argument('--appendix', help='Path to the appendix Markdown file.')
    parser.add_argument('--revision-history', help='Path to the revision history Markdown file.')
    parser.add_argument('--footer', help='Footer text literal.', default='')

    args = parser.parse_args()
    data = read_csv(args.csv_file)
    grouped_data = group_by_category(data)

    title_content = read_text_file(args.title) if args.title else ""
    bg_content = read_text_file(args.background) if args.background else ""
    appendix_content = read_text_file(args.appendix) if args.appendix else ""
    revision_history_df = parse_revision_history(args.revision_history) if args.revision_history else None

    if args.format == 'markdown':
        generate_markdown(grouped_data, args.output_file, title_content, bg_content, appendix_content, revision_history_df.to_markdown(index=False) if revision_history_df is not None else "")
    elif args.format == 'pdf':
        generate_pdf(grouped_data, args.output_file, title_content, bg_content, appendix_content, revision_history_df, args.footer)


