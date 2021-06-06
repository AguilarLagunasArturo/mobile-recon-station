function setup() {
	var c = createCanvas(
		screen.availWidth * (1-0.2),
		screen.availHeight * (1-0.2),
		WEBGL
	);
	c.parent("canvas")
}

function draw() {
	background(100, 200, 200);
	rotateX(frameCount * 0.01);
  rotateY(frameCount * 0.01);
  box(50);
}

function keyPressed() {
	if (keyCode === UP_ARROW) {
		console.log("up");
	} else if (keyCode === DOWN_ARROW) {
		console.log("down");
	} else if (keyCode === RIGHT_ARROW) {
		console.log("right");
	} else if (keyCode === LEFT_ARROW) {
		console.log("left");
	}
}
