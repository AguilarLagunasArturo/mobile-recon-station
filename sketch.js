// global vars
var abs_pos_x, abs_pos_y, step, step_amt, rot, rot_amt, passive, static_rot, toggle;
function setup() {
	abs_pos_x = 0;
	abs_pos_y = 0;
	step = 0;
	step_amt = 5;
	rot = 0;
	rot_amt = PI/100;
	passive = false;
	static_rot = 0;
	toggle = false;

	var c = createCanvas(
		400,
		400,
		WEBGL
	);
	/*var c = createCanvas(
		screen.availWidth * (1-0.2),
		screen.availHeight * (1-0.2),
		WEBGL
	);*/
	c.parent("canvas")
}

function draw() {
	background(100, 200, 200);
	// rotatey
	// translate z
	translate(abs_pos_x, 0, abs_pos_y);
	if (passive) {
		rotateY(rot);
	} else {
		rotateY(rot);
		translate(0, 0, step);
		abs_pos_x = abs_pos_x + step * sin(static_rot);
		abs_pos_y = abs_pos_y + step * cos(static_rot);
	}
	// passive = true;
	box(80, 50, 100);
}

function keyPressed() {
	if (keyCode === UP_ARROW) {
		console.log("up");
		step = -step_amt;
		static_rot = rot;
		passive = false;
	} else if (keyCode === DOWN_ARROW) {
		console.log("down");
		step = step_amt;
		static_rot = rot;
		passive = false;
	} else if (keyCode === RIGHT_ARROW) {
		passive = true;
		rot -= rot_amt;
		console.log("right");
	} else if (keyCode === LEFT_ARROW) {
		passive = true;
		rot += rot_amt;
		console.log("left");
	}
}

function keyReleased() {
	if (keyCode === UP_ARROW) {
		console.log("up-released");
		step = -step_amt;
		static_rot = rot;
		passive = false;
	} else if (keyCode === DOWN_ARROW) {
		console.log("down-released");
		step = step_amt;
		static_rot = rot;
		passive = false;
	} else if (keyCode === RIGHT_ARROW) {
		passive = true;
		rot -= rot_amt;
		console.log("right-released");
	} else if (keyCode === LEFT_ARROW) {
		passive = true;
		rot += rot_amt;
		console.log("left-released");
	}
}
