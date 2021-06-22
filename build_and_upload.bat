git add *
git commit -m "auto update"
git push
python setup.py sdist bdist_wheel
twine upload dist/*
