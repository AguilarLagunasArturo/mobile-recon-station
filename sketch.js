// global vars
var abs_pos_x, abs_pos_y, step, step_amt, abs_rot, rot, rot_amt, toggle;
var rotating, translating;
var view, V2D, V3D;
var CAR_W, CAR_H, CAR_D;
var OBJ_W, OBJ_H, OBJ_D;
var FLOOR_W, FLOOR_H, FLOOR_D;

function preload(){
	c = loadModel('minimal-model.stl');
}

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

	CAR_W = 165;
	CAR_H = 75;
	CAR_D = 200;

	OBJ_W = width/4;
	OBJ_H = 60;
	OBJ_D = 20;

	FLOOR_W = width;
	FLOOR_H = 20;
	FLOOR_D = height;

	noStroke();
}

function draw() {
	//ortho();
	background(215, 227, 213);
	ambientLight(171, 183, 196);
	//pointLight(204, 96, 96, 0, 500, 0);
	pointLight(32, 32, 32, 0, -500, 0);


	if (view == V2D){
		rotateX(-HALF_PI);
	} else if (view == V3D){
		//translate(0, 100, -500);
		translate(0, 100, 0);
	}

	push();
	translate(0, (CAR_H + FLOOR_H)/2, 0);
	box(FLOOR_W, FLOOR_H, FLOOR_D);
	pop();

	//push();
	//translate(0, - (OBJ_H - CAR_H)/2, -100);
	//box(OBJ_W, OBJ_H, OBJ_D);
	//pop();

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
	//box(CAR_W, CAR_H, CAR_D);
	rotateX(HALF_PI);
	rotateZ(PI);
	push();
	specularMaterial(250, 250, 250);
	fill(196, 207, 206);
	model(c);
	pop();


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
