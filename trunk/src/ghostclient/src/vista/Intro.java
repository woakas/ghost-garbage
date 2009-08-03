package vista;
import java.util.Timer;

import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public final class Intro extends Canvas {
	
	private Display display;
	private Displayable next;
	private Timer timer;
	private Image image;
	private int dismissTime;

	public Intro(Display display, Displayable next, Image image,int dismissTime) {
	timer = new Timer();
	this.display = display;
	this.next = next;
	this.image = image;
	this.dismissTime = dismissTime;
	display.setCurrent(this);
	}
	static void access(Intro intro) {
		intro.dismiss();
		}
		private void dismiss() {
		timer.cancel();
		display.setCurrent(next);
		}
		protected void keyPressed(int keyCode) {
		dismiss();
		}
		protected void paint(Graphics g) {
		g.setColor(255, 255, 255);
		g.fillRect(0, 0, getWidth(), getHeight());
		g.setColor(0, 0, 0);
		g.drawImage(image, getWidth() / 2, getHeight() / 2 - 5, 3);
		}
		protected void pointerPressed(int x, int y) {
		dismiss();
		}
		protected void showNotify() {
			if(dismissTime > 0)
			timer.schedule(new Conteo(this), dismissTime);
		}
}
