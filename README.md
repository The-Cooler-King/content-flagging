# content-flagging
A python app that reads PDF's and flags for a user-created set of words. The app will be used to assist in content flagging for 
editors.

## Future Iterations
The MVP is an app that reads a pdf and flags for a set of words. There are multiple improvements that will be worthwhile
due to the fact that the app will assist my wife, and it will be an excellent exercise for my software development
skill.
1. Multi-threading - scan multiple pdf's at once. Each pdf is an independent entity.
2. Collect metadata on books and maintain a database
3. Introduce an LM to flag passages for inappropriate themes rather than just words.
4. Feed the LM with manually flagged content.
5. Create a UI to drop files into and interact with flagged content

The earliest iterations of this project will be able to catch some books that perhaps do not belong in categories or obviously violate
content standards. There is a window of content that is flagged manually and this window encompasses essentially all of the content that
should be flagged. With further iterations the window of content flagged automatically should increase in size, reducing time spent reading books
that violate content standards.