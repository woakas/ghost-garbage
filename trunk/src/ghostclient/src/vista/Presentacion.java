package vista;

import java.io.IOException;

import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Font;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public class Presentacion extends Canvas {
	
	private Image log1, log2,log3,log4;
	private BotonIni bot;
	GhostGarbage ref;
	
	public Presentacion(GhostGarbage ref) {
        setFullScreenMode(true);
		this.ref = ref;
		bot = new BotonIni("Comenzar", this);
		try {
			log1 = Image.createImage("/logoj.png");
			log2 = Image.createImage("/info.png");
			log3 = Image.createImage("/ayuda.png");
			log4 = Image.createImage("/cerrar.png");
			} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected void paint(Graphics g) {
		g.setColor(0,0,0);
		g.fillRect(0, 0, getWidth(), getHeight());
		Font fuente = Font.getFont(Font.FACE_SYSTEM, Font.STYLE_BOLD, Font.SIZE_LARGE);
		g.setFont(fuente);
		g.setColor(90, 90, 90);
		g.drawString("Ghost Garbage",getWidth() / 4 , 20, Graphics.TOP|Graphics.LEFT);
		g.setColor(255, 255, 255);
		g.drawString("Ghost Garbage", getWidth() / 4 +2, 22, Graphics.TOP|Graphics.LEFT);
		fuente = Font.getFont(Font.FACE_SYSTEM, Font.STYLE_BOLD, Font.SIZE_MEDIUM);
		g.setFont(fuente);
		bot.paint(g, getWidth(), getHeight());
		
		if(bot.opcion == 1){
			g.drawImage(log1, 10, 60, Graphics.TOP|Graphics.LEFT);
		}
		if(bot.opcion == 2){
			g.drawImage(log2, 10, 60, Graphics.TOP|Graphics.LEFT);
		}
		if(bot.opcion == 3){
			g.drawImage(log3, 10, 60, Graphics.TOP|Graphics.LEFT);
		}
		if(bot.opcion == 4){
			g.drawImage(log4, 10, 60, Graphics.TOP|Graphics.LEFT);
		}
	}
	public void keyPressed(int keyCode) {
		switch (getGameAction(keyCode)) {
		case FIRE:
			ref.getOpcion(bot.opcion);
			break;
		case Canvas.DOWN:
			if(bot.selec<=60){
				bot.selec = bot.selec+30;
				bot.opcion = bot.opcion+1;
			}
			break;			
		case Canvas.UP:
			if(bot.selec>= 30){
				bot.selec = bot.selec-30;
				bot.opcion = bot.opcion-1;
			}
			break;
		}
		repaint();
	}
}