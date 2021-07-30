<!DOCTYPE html>
<body>
<h1>Welcome!</h1>
<h3>Python setup</h3>
<p>
	Before the first execution you need to install the python libraries used by the tool:
</p>
<pre>pip3 install -r requirements.txt</pre>
<h3>Preparation</h3>
<ul>
	<li>
		Insert an .mp3/.m4a 5 seconds long and an horizontal .jpg in the <strong>/input</strong> folder.
	</li>
	<li>
		Modify the dictionary inside <strong>/input/settings.py</strong> to set the output size of the textile, in points.
	</li>
	<li>
		Modify .dat files in the <strong>/input</strong> folder to change the mapping patterns. Only 0s or 1s. Keep in mind that the dimensions of the output image should be divisable by the ones of the patterns (e.g. if the output width is 150, the pattern width can be 5 but not 9, and same for the height).
	</li>
</ul>
<h3>Run</h3>
<p>Move to the folder containing the code from the terminal:</p>
<pre>cd [your_folder]</pre>
<p>Run the main.py script</p>
<pre>python3 main.py</pre>
</body>
</html>