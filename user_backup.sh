#!/bin/bash
echo "Backing up user data..."
echo "Name: Natasha Romanoff" > backup.txt
echo "Email: natasha@shield.gov" >> backup.txt
echo "Phone: +1-999-555-0198" >> backup.txt
echo "DOB: 1984-12-03" >> backup.txt

zip user_backup.zip backup.txt
rm backup.txt