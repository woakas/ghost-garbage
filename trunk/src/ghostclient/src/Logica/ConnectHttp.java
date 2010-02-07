package Logica;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import javax.microedition.io.Connector;
import javax.microedition.io.HttpConnection;

import org.json.me.JSONException;
import org.json.me.JSONObject;

import vista.Usuarios;


public class ConnectHttp{
	public static Usuarios us;
	public static String cookie="";
    public static String URL_LOGIN=vista.GhostGarbage.URLGHOST+"accounts/login/";
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
	public static JSONObject getUrlJson(String url){
		String body = getUrlBody(url);
		if (body != null) {
			try {
				return new JSONObject(body);
			} catch (JSONException e) {}			
			}
		return null;
	}
	public static String getUrlBody(String url){
		HttpConnection httpc = getUrl(url,USER,PASSWORD);
		if (httpc==null){
			return null;
		}
		try {
			InputStream dis = httpc.openInputStream();
			StringBuffer sb = new StringBuffer();
			int ch = 0;
			while ((ch=dis.read())!=-1){
				sb.append((char)ch);
			}
			return new String (sb);
		} catch (IOException e) {}
		return null;
		}
	
	public static HttpConnection getUrl(String url,String usuario, String password){ 
		HttpConnection c = null;
	    OutputStream os = null;
		try {			
			//Trata de entrar a la url solicitada
			 c = (HttpConnection)Connector.open(url);
			 c.setRequestProperty("Cookie",cookie);
				
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
	        if (c.getResponseCode()==HttpConnection.HTTP_OK){
					return c;		
			}
			return null;
		}  
		catch (IOException e) {	}
		return null;	
	}
}
