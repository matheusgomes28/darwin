# Darwin - Image Processing Branch.
For the moment, this is where all the image processing stuff will go. Becca and I (Mat) are currently working on applying all the techniques implemented on a dataset of images. Becca is working on the Histogram equalisation of images, while Mat is developing the CLI code so we can run the deblurring/equalisation stuff on datasets. An overall plan for the branch was broken down into the following list

- Applying filters to images (Blurring, Laplacian).
- Fourier Transform for deblurring (along with unsharp mask).
- Histogram equalisation for contrast fixing.
- Applying the above onto a batch of images.
  - Creating files to load dataset.
  - CLI to pass location and other params.
  - Possibly a loading bar, so we know the progress.
  
Obviously there will be other things that will need to be implemented, but the list above will be updated and the deadline for everything was set to be at the end of next week (Fry 23/02).

				    _________
				   /         /.
	    .-------------.       /_________/ |
	   /             / |      |         | |
	  /+============+\ |      | |====|  | |
	  ||C:\>        || |      |         | |
	  ||            || |      | |====|  | |
	  ||            || |      |   ___   | |
	  ||            || |      |  |166|  | |
	  ||            ||/@@@    |   ---   | |
	  \+============+/    @   |_________|./.
			     @          ..  ....'
	  ..................@     __.'.'  ''
	 /oooooooooooooooo//     ///
	/................//     /_/
	------------------
