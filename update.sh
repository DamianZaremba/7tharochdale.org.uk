#!/bin/bash
cd "$(dirname $(readlink -f $0))"
rm -rf DamianZaremba-7tharochdale.org.uk-*.tar.gz
wget --no-check-certificate https://github.com/DamianZaremba/7tharochdale.org.uk/tarball/live
tar -xvf DamianZaremba-7tharochdale.org.uk-*.tar.gz
rsync -vr --delete --exclude=update.sh DamianZaremba-7tharochdale.org.uk-*/* .
rm -rf DamianZaremba-7tharochdale.org.uk-*
chown www-data:www-data -R *
find . -type f -exec chmod 640 {} \;
find . -type d -exec chmod 750 {} \;
echo "Deployed to $(pwd)"
