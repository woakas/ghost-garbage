package Logica;

import java.io.IOException;
import java.io.OutputStream;
import javax.microedition.io.Connector;
import javax.microedition.io.HttpConnection;

import vista.Usuarios;


public class ConnectHttp{
	
	public static Usuarios us;
	public static String cookie="";
	public static String URL_LOGIN="http://dev.ghost.webhop.org/accounts/login/";
	public static String USER="anonymus";
	public static String PASSWORD="anonymus";
	
	
	public ConnectHttp(){
		cleanValues();
	}
	
	public static void cleanValues(){
		USER="anonymus";
		PASSWORD="anonymus";
		cookie="";
	}
	
	public static HttpConnection getUrl(String url ){
		return getUrl(url,USER,PASSWORD);
	}
	
	
	public static HttpConnection getUrl(String url,String usuario, String password){ 
		
		HttpConnection c = null;
	    OutputStream os = null;
	    System.out.println("PEPITO");
		try {			
			//Trata de entrar a la url solicitada
			 c = (HttpConnection)Connector.open(url);
			 c.setRequestProperty("Cookie",cookie);
			 System.out.println("Intento 1 "+c.getResponseCode());
		         
				
			// si la respuesta es 401 que significa que es unauthorized trata de entrar a la URL de login 
	         if (c.getResponseCode()==HttpConnection.HTTP_UNAUTHORIZED){
	        	 c = (HttpConnection)Connector.open(URL_LOGIN);
		         c.setRequestMethod(HttpConnection.POST);
		         os = c.openOutputStream();
		         os.write(("username="+usuario+"&password="+password).getBytes());
		         os.flush();
		         
				//Toma la cookie y la setea
		        String cook=c.getHeaderField("set-cookie");
				cookie = cook.substring(0, cook.indexOf(";"));
				System.out.println("cookie "+cookie);
				System.out.println("Intento logeo "+c.getResponseCode());								

				//Vuelve a tratar de entrar a la URL solicitada
				c = (HttpConnection)Connector.open(url);
				c.setRequestProperty("Cookie",cookie);
		       			
				if (c.getResponseCode()==HttpConnection.HTTP_UNAUTHORIZED){
					cleanValues();
					return null;
				}else {
					USER=usuario;
					PASSWORD=password;	
				}

			}
			return c;
		}  
		catch (IOException e) {
			System.out.println(e);
		}
		return null;	
	}
}
