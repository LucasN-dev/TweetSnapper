# TweetSnapper
Automatically create Internet Archive snapshots of someone's latest tweets!

### Dependencies
- Selenium

### How to use
Simply edit the account username and the chrome driver path and run the script.
<br>You can adjust the check frequency by changing the "delay" variable at the end of the script.

### How it works
The script retrieves the last few tweets on the selected Twitter account and checks if snapshots already exist using the [Internet Archive API](https://archive.readme.io/docs/website-snapshots). If a tweet is not archived yet, a snapshot is created.
