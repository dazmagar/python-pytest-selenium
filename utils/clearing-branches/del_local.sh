for mergedBranch in $(git for-each-ref --format '%(refname:short)' --merged HEAD refs/heads/ | grep -v "DEV" | grep -v "master")
do
	echo "Locals to remove: " ${mergedBranch}
    git branch -d ${mergedBranch}
done
