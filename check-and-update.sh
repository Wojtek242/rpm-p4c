#!/usr/bin/env sh

SPEC_GIT_REVISION=`grep "%define git_commit[^_]" p4c.spec | cut -d " " -f 3`
REMOTE_GIT_REVISION=`git ls-remote git://github.com/p4lang/p4c.git refs/heads/master | cut -f 1`

if [ "${SPEC_GIT_REVISION}" = "${REMOTE_GIT_REVISION}" ]
then
    echo "No new git revision : skipping update"
    exit 0
fi

echo "New git revision {${REMOTE_GIT_REVISION}} : updating"

PKGREL=`awk '/Release:/ {print $2}' p4c.spec | cut -d "." -f 2`
NEW_PKGREL=$((${PKGREL} + 1))

sed -i "s/${SPEC_GIT_REVISION}/${REMOTE_GIT_REVISION}/" p4c.spec
sed -ri "s/(Release:\s+0.)[0-9]+/\1${NEW_PKGREL}/" p4c.spec
