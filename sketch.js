var x = 0;
var y = 0;
var z = 0;
var step = 10;

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
	// rotateX(frameCount * 0.005);
	// rotateY(frameCount * 0.005);
	translate(x, y, z);
	box(80, 50, 100);
}

function keyPressed() {
	if (keyCode === UP_ARROW) {
		z -= step;
		console.log("up");
	} else if (keyCode === DOWN_ARROW) {
		z += step;
		console.log("down");
	} else if (keyCode === RIGHT_ARROW) {
		x += step;
		console.log("right");
	} else if (keyCode === LEFT_ARROW) {
		x -= step;
		console.log("left");
	}
}
