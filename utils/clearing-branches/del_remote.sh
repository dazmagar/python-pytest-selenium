git fetch origin --prune
for reBranch in $(git branch -a)
do
{
  if [[ $reBranch == remotes/origin* ]];
  then
  {
    if [[ $reBranch == remotes/origin/HEAD ]]; then 
    echo "HEAD is not a branch"
    else
      branch=$(echo $reBranch | cut -d'/' -f 3)
      sha=$(git rev-parse origin/$branch)
      dateo=$(git show -s --format=%ci $sha)
      datef=$(echo $dateo | cut -d' ' -f 1)
      Todate=$(date -d "$datef" +'%s')
      current=$(date +'%s')
      day=$(( ( $current - $Todate )/60/60/24 ))
      if [ "$day" -gt 60 ]; then
      echo "branch: " $branch "age in days: " $day
	    git push origin :$branch
      fi
    fi

  }
  fi
}
done