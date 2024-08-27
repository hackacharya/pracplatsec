# pracplatsec
  A Getting Started TODO List for platform/kubernetes cluster security - especially if you are deploying and managing your own fresh kubernetes system etc. maintaining it as a markdown to be able to update easily.

 . Note we maintain the CSV file and then use the gendoc.py to generate the MD and the PDF files. Easier to eedit and track and put categories and such. And the CSV can be a CSV.

  All changes are accepted to the CSV 

# Contributing to this list
  If you have some things that you would like to add please do send a pull request


# To gnerate the laset md or the PDF file  see genner.gen.sh
   pip install reportlab pandas lxml tabulate

# If you have time to kill - then - An unncessarily complicated but interesting way to get your PDF from the MD
   pip install grip
   grip PracticalPlatformSecurity.md
   open http://localhost:6419
   See also pandoc, a2pdf, pdflatex etc.. 

