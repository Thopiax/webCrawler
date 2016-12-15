
# WebCrawler

No installation instructions, no need to compile or anything of the sort.

To run, either run with `python3 WebCrawler.py *args*` or just simply `./WebCrawler.py *args*`. 
The crawler takes at least one argument, but can easily run with multiple.
Also, the WebCrawler is visited to a `MAX_VISIT_COUNT (=100)` number of visits to a given domain so that it doesn't overload their servers. That number can be altered in WebCrawler.py.

Finally, to run the tests, all you have to do is make sure they are in the same folder as the Util and the main file and run `python3 WebCrawlerTests.py`.