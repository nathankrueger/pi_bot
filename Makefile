GIT_REPO=https://github.com/nathankrueger/pi_bot

clean:
	find . -name "*.pyc" -exec rm {} \;

# Git stuff
co:
	git add $(FILES)

ci:
	git commit

rm:
	git rm $(FILES)

push:
	git push origin master

pull:
	git pull origin master

revert:
	git reset

repo:
	open $(GIT_REPO)

