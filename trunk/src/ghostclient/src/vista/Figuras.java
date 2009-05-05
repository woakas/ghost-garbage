package vista;

import java.io.IOException;

import javax.microedition.lcdui.CustomItem;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public class Figuras extends CustomItem {
	private int w,h;
	private Image img,img1,img2;
	
	protected Figuras(String nombre, Displayable d) {
	super(nombre);
	    seth(d.getHeight());
	    setw(d.getWidth());
		try {
			img = Image.createImage("/Fondo.png");
			img1 = Image.createImage("/escobita.png");
			img2 = Image.createImage("/fantasma.png");
			} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	protected void paint(Graphics g, int w, int h) {
		g.drawImage(img, 0, 0, Graphics.TOP|Graphics.LEFT);
		g.drawImage(img1, 10, 0, Graphics.TOP|Graphics.LEFT);
		g.drawImage(img2, w/2+10, 0, Graphics.TOP|Graphics.LEFT);
	}
	public void seth(int h) {
		this.h = h-120;
	}
	public void setw(int w) {
		this.w = w;
	}
	protected int getMinContentHeight() {
		return h;
	}
	protected int getMinContentWidth() {
		return w;
	}
	protected int getPrefContentHeight(int arg0) {
		return getMinContentHeight();
	}
	protected int getPrefContentWidth(int arg0) {
		return getMinContentWidth();
	}
}