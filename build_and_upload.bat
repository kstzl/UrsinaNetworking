@echo off

echo [1 / 4] Deleting old folders ...

RMDIR "build" /s /q
RMDIR "dist" /s /q
RMDIR "UrsinaNetworking.egg-info" /s /q

echo [2 / 4] Pushing on github ...

git add *
git commit -m "auto update"
git push

echo [3 / 4] Building the lib ...

python setup.py sdist bdist_wheel

echo [4 /4] Uploading to PyPi ...

twine upload dist/*

echo Finished ! :D

pause