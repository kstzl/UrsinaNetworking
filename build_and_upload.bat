git add *
git commit -m "auto update"
git push
python "D:\Documents\URSINA STUFF\ursinaNetworking\UrsinaNetworking\setup.py" sdist bdist_wheel
twine upload dist/*
