var rot, step, rot_amt, step_amt;

function setup() {
	rot = 0;
	step = 0;
	step_amt = 10;
	rot_amt = TWO_PI/20;
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
	// box(80, 50, 100);
	rotateY(rot);
	translate(0, 0, step);
	box(80, 50, 100);
}

function keyPressed() {
	if (keyCode === UP_ARROW) {
		step -= step_amt;
		console.log("up");
	} else if (keyCode === DOWN_ARROW) {
		step += step_amt;
		console.log("down");
	} else if (keyCode === RIGHT_ARROW) {
		rot += rot_amt;
		console.log("right");
	} else if (keyCode === LEFT_ARROW) {
		rot -= rot_amt;
		console.log("left");
	}
}
