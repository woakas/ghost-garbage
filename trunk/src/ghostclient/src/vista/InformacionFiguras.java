package vista;

import java.io.IOException;
import javax.microedition.lcdui.CustomItem;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public class InformacionFiguras extends CustomItem {
	private int w,h;
	private Image img1,img2;
	
	protected InformacionFiguras(String nombre, Displayable d) {
	super(nombre);
	    seth(d.getHeight());
	    setw(d.getWidth());
		try {
			img1 = Image.createImage("/info.png");
			img2 = Image.createImage("/logoj.png");
			} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	protected void paint(Graphics g, int w, int h) {
		g.setColor(0,0,0);
		g.fillRect(0, 0, w, h);
		g.drawImage(img1, 20, 20, Graphics.TOP|Graphics.LEFT);
		g.drawImage(img2, w/2+20, 30, Graphics.TOP|Graphics.LEFT);
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