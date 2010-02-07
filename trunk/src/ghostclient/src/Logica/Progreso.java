package Logica;

import java.util.TimerTask;
import javax.microedition.lcdui.Gauge;

public class Progreso extends TimerTask{
	private Gauge load;

	public Progreso(Gauge load) {
		this.load =load;
	}
	public final void run() {
		   if (load.getValue() < load.getMaxValue()){
	    	   load.setValue(load.getValue() + 1);
	       }
	       else
	       {
	    	 // Renueva el valor del Gauge a 0 
	         load.setValue(0);
	         // Detiene el timer
	         cancel();      
	       }
     }
}
