package vista;

import javax.microedition.lcdui.CustomItem;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Graphics;

public class BotonIni extends CustomItem {
	private int w,h;
	Displayable d;
	private int x, y, alto;
	public boolean seleccionador;
	public int selec = 0, opcion = 1;

	protected BotonIni(String nombre, Displayable d) {
		
		super(nombre);
		this.d = d;
		seth(d.getHeight());
		setw(d.getWidth());
		x = 100;
		y = 60;
		alto = 20;
		seleccionador = true;
	}
	public void seth(int h) {
		this.h = h;
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

	protected void paint(Graphics g, int w, int h) {
		
		if(seleccionador){
			g.setColor(55, 55, 55);
			g.fillRoundRect(x-17, (y+selec)-3, w+10, alto+7, 20, 45);
		}
		g.fillRoundRect(x-15, y, w+10, alto, 20, 45);
		g.setColor(90, 90, 90);
		g.fillRoundRect(x-14, y+1, w+10, alto, 20, 45);
		g.setColor(125, 125, 125);
		g.fillRoundRect(x-10, y+5, w+10, alto-15, 20, 45);
		g.setColor(255,255,255);
		g.drawString("Ghost Garbage", x-5, y+4, Graphics.TOP|Graphics.LEFT);
		
		g.setColor(0,0,0);
		g.fillRoundRect(x-15, y+30, w+10, alto, 20, 45);
		g.setColor(90, 90, 90);
		g.fillRoundRect(x-14, y+31, w+10, alto, 20, 45);
		g.setColor(125, 125, 125);
		g.fillRoundRect(x-10, y+35, w+10, alto-15, 20, 45);
		g.setColor(255,255,255);
		g.drawString("Información", x-5, (y+30)+4, Graphics.TOP|Graphics.LEFT);
		
		g.setColor(0,0,0);
		g.fillRoundRect(x-15, y+60, w+10, alto, 20, 45);
		g.setColor(90, 90, 90);
		g.fillRoundRect(x-14, y+61, w+10, alto, 20, 45);
		g.setColor(125, 125, 125);
		g.fillRoundRect(x-10, y+65, w+10, alto-15, 20, 45);
		g.setColor(255,255,255);
		g.drawString("Ayuda", x-5, (y+60)+4, Graphics.TOP|Graphics.LEFT);

		g.setColor(0,0,0);
		g.fillRoundRect(x-15, y+90, w+10, alto, 20, 45);
		g.setColor(90, 90, 90);
		g.fillRoundRect(x-14, y+91, w+10, alto, 20, 45);
		g.setColor(125, 125, 125);
		g.fillRoundRect(x-10, y+95, w+10, alto-15, 20, 45);
		g.setColor(255,255,255);
		g.drawString("Salir", x-5, (y+90)+4, Graphics.TOP|Graphics.LEFT);
	}
}