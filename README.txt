What is this?
=============

TEH mega-manga-mass-downloader (aka すごいですね？Read: Sugoi desu ne?) 
is a little app that will mass-download FLVs of videos from various video sites like
dailymotion, youtube, blip...

How does it do that?
====================
Various video sharing websites offer an RSS feed that supports the MRSS
extension (Media RSS http://en.wikipedia.org/wiki/Media_RSS), so the app fetches
the feeds and helps you download the videos in it.

Ok, But Why?
============
I am a fan of Japanese animes, I like them even more when they're produced by
fansub'ers http://en.wikipedia.org/wiki/Fansub --And to be honnest, I like to
keep what I like in a DVD. So that's it. I download them.

What can I do with it now?
==========================
Given a single dailymotion feed of a playlist, it can:
- Generate a bash script that uses "wget" to download all the episodes
of the anime in the feed!

Or 

-Download the videos (with a resume ability) directly with python.

Example Usage:
==============
Generate a bash script that will download ALL the FLVs in the playlist
"Toradora" (4 pages) 
./fetch.py -bn 4 http://www.dailymotion.com/rss/playlist/xw6ow_chewiei_toradora

You can redirect this output to a bash file, like this:
 ./fetch.py -bn 4 http://www.dailymotion.com/rss/playlist/xw6ow_chewiei_toradora  > download.sh 

 and then:

 chmod +x download.sh
 and run it: ./download.sh

 Or even more easily:
 ./fetch.py -n 5 http://www.dailymotion.com/rss/playlist/xw6ow_chewiei_toradora
 Will download them directly (using the builtin python modules)

** -- **

More Doc to come, I promise! :)

P.S. Oh, by the way, this app's original name was: TEH Mega-Manga-Mass-Downloader.
Yes that's a BIG and pompous name, so I reduced it to  すごいですね？(Read: Sugoi desu ne?) 
Which in japanese means: Isn't it Fabulous/Great/Coo/Big? :)

