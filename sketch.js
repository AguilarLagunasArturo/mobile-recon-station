// global vars
var abs_pos_x, abs_pos_y, step, step_amt, abs_rot, rot, rot_amt, toggle;
var rotating, translating;
var view, V2D, V3D;

function setup() {
	step = 0;
	step_amt = 5;
	abs_pos_x = 0;
	abs_pos_y = 0;

	abs_rot = 0;
	rot = 0;
	rot_amt = PI/100;

	rotating = false;
	translating = false;

	V2D = 0;
	V3D = 1;
	view = V3D;

	var c = createCanvas(
		screen.availWidth * (1-0.2),
		screen.availHeight * (1-0.2),
		WEBGL
	);
	c.parent("canvas")
}

function draw() {
	background(100, 200, 200);

	if (view == V2D){
		rotateX(-HALF_PI);
	} else if (view == V3D){
		translate(0, 100, 0);
	}
	push();
	translate(0, 40, 0);
	box(width, 20, height);
	pop();

	translate(abs_pos_x, 0, abs_pos_y);
	if (rotating) {
		rotateY(abs_rot);
		abs_rot += rot;
	} else if (translating) {
		rotateY(abs_rot);
		translate(0, 0, step);
		abs_pos_x = abs_pos_x + step * sin(abs_rot);
		abs_pos_y = abs_pos_y + step * cos(abs_rot);
	} else {
		rotateY(abs_rot);
	}
	box(80, 50, 100);
}

function keyPressed() {
	if (keyCode === UP_ARROW) {
		step = -step_amt;
		passive = false;
		translating = true;
	} else if (keyCode === DOWN_ARROW) {
		step = step_amt;
		passive = false;
		translating = true;
	} else if (keyCode === RIGHT_ARROW) {
		passive = true;
		abs_rot -= rot_amt;
		rot = -rot_amt;
		rotating = true;
	} else if (keyCode === LEFT_ARROW) {
		passive = true;
		abs_rot += rot_amt;
		rot = rot_amt;
		rotating = true;
	}
}

function keyReleased() {
	if (keyCode === UP_ARROW || keyCode === DOWN_ARROW) {
		translating = false;
	} else if (keyCode === LEFT_ARROW || keyCode === RIGHT_ARROW) {
		rotating = false;
	}
}
