#!/bin/sh 

# pip install reportlab pandas lxml tabulate

OPTIONS="--title title.md --background intro.md --appendix appendix.md --revision-history revision.md --footer hackacharya@gmail.com"
case $1 in
md) 
  ./gendoc.py PracticalPlatformSecurity.csv ../PracticalPlatformSecurity.md  --format markdown  $OPTIONS 
  ;;
pdf)
  ./gendoc.py PracticalPlatformSecurity.csv ../PracticalPlatformSecurity.pdf --format pdf $OPTIONS 
  ;;
esac
