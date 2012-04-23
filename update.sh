#!/bin/bash

# Figure out what dir the script exists in
# we use this to ensure we are deploying to the correct place
# this could be hard coded but what's the point?
deploy_dir="$(dirname $(readlink -f $0))"
cd $deploy_dir;

# Check if we are a git dir or not
if [ -d ".git" ];
then
	echo "Updating working copy";
	git pull;
else
	echo "Cloning live branch";
	git clone -b live git://github.com/DamianZaremba/7tharochdale.org.uk $deploy_dir;
fi

# Fix ownership
chown www-data:www-data -R $deploy_dir;

# Fix permissions
# The site is totally static so nothing need to be writeable etc
find $deploy_dir -type d -exec chmod 750 {} \;;
find $deploy_dir -type f -exec chmod 640 {} \;;

# Tell the user we are done
echo "Deployed to $(pwd)";
exit(0);