package vista;

import java.io.IOException;

import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Font;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public class Presentacion extends Canvas {
	
	private Image img, log1;
	private BotonIni bot;
	Pantalla ref;
	
	public Presentacion(Pantalla ref) {
		
		this.ref = ref;
		bot = new BotonIni("Comenzar", this);
		try {
			img = Image.createImage("/negro.jpg");
			log1 = Image.createImage("/o.png");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected void paint(Graphics g) {
		
		g.drawImage(img, 0, 0, Graphics.TOP|Graphics.LEFT);
		
		Font fuente = Font.getFont(Font.FACE_SYSTEM, Font.STYLE_BOLD, Font.SIZE_LARGE);
		g.setFont(fuente);
		g.setColor(90, 90, 90);
		g.drawString("Ghost Garbage", 40, 20, Graphics.TOP|Graphics.LEFT);
		
		g.setColor(255, 255, 255);
		g.drawString("Ghost Garbage", 42, 22, Graphics.TOP|Graphics.LEFT);
		
		fuente = Font.getFont(Font.FACE_SYSTEM, Font.STYLE_BOLD, Font.SIZE_MEDIUM);
		g.setFont(fuente);
		bot.paint(g, getWidth(), getHeight());
		
		if(bot.opcion == 1){
			g.drawImage(log1, 10, 100, Graphics.TOP|Graphics.LEFT);
		}

	}
	public void keyPressed(int keyCode) {
		
		switch (keyCode) {
		case -5:
			
			ref.getOpcion(bot.opcion);
			repaint();
			break;
		default:
			break;
		}
		
		int key = getGameAction(keyCode);
		
		switch (key) {
		case Canvas.DOWN:
			if(bot.selec<=60){
				System.out.println("opcion: "+ bot.opcion);
				bot.selec = bot.selec+30;
				bot.opcion = bot.opcion+1;
				System.out.println("opcion: "+ bot.opcion);
			}
			repaint();
			break;
			
		case Canvas.UP:
			if(bot.selec>= 30){
				bot.selec = bot.selec-30;
				bot.opcion = bot.opcion-1;
				System.out.println("opcion: "+ bot.opcion);
			}
			repaint();
			break;

		}

	}
}