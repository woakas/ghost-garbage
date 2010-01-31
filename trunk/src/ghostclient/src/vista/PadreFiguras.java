package vista;

import java.io.IOException;
import javax.microedition.lcdui.CustomItem;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public class PadreFiguras extends CustomItem {
	private int w,h;
	private Image img1,img2;
	
	protected PadreFiguras(String nombre, Displayable d, String image,String image2) {
	super(nombre);
	    seth(d.getHeight());
	    setw(d.getWidth());
		try {
			img1 = Image.createImage("/"+image);
			img2 = Image.createImage("/"+image2);
			} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	protected void paint(Graphics g, int w, int h) {
		g.setColor(0,0,0);
		g.fillRect(0, 0, w, h);
		g.drawImage(img1, 20, 25, Graphics.TOP|Graphics.LEFT);
		g.drawImage(img2, w/2+25, 25, Graphics.TOP|Graphics.LEFT);
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