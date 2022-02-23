#!/bin/bash

mkdir repo
cd repo

git init -b master

echo "Flag is... Somewhere." > README.md
git add .
git commit -m "Initial commit"

for i in {1..1234}
do
   git checkout -b kekus-${RANDOM}
   echo "Sorry, nothing here! (bip-bup-bip ${RANDOM})"  > hehe-${RANDOM}.txt
   git add .
   git commit -m "GOOD LUCK №${RANDOM}"
   git checkout -
done

git checkout - 
echo 'HITS{z45cr1pt0v4l_kr454v4}' > hehe-${RANDOM}.txt
git add .
git amend

git checkout master

cd ..

# zip -r repo.zip repo
# rm -rf repo