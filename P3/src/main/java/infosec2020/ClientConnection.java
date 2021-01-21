package infosec2020;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.LinkedHashMap;

/**
 *  Class to handle traffic from a specific client to proxy.
 *  Parses (GET) requests and establishes new connection to server
 * (ServerConnection thread) or reuses connection, if a connection to the
 * requested endpoint already exists. Adds request to send queue of
 * corresponding ServerConnection thread.
 *  */
public class ClientConnection extends Thread {
  private final Socket clientSocket;
  private final InputStream client_is;
  private final OutputStream client_os;
  private final Proxy proxy;

  ClientConnection(Socket cSocket, Proxy parent_proxy) throws Exception {
    if (cSocket == null)
      throw new Exception(
          "[CC] Error when starting client connection: client socket was null!");

    clientSocket = cSocket;
    client_is = clientSocket.getInputStream();
    client_os = clientSocket.getOutputStream();
    proxy = parent_proxy;
  }

  public void run() {
    try {
      System.out.println("[CC] A client connection was started.");
      while (true) {
        HTTPMessage newRequest = new HTTPMessage();

        // parse header (ignore CRLF if at beginning of message -> look at page
        // 31 of RFC2616)
        if (!(newRequest.parseRequest(client_is)))
          break;
        // TODO: Implement Proxy 
        throw new RuntimeException("Not Implemented");
      }
    } catch (Exception e) {
      System.out.println("[CC] Error when processing: " + e.getMessage());
      // try to send error message to client.
      try {
        String errorMsg =
            "HTTP/1.1 400 INFOSEC PROXY ERROR\r\nContent-Length: 19\r\n\r\nINFOSEC PROXY ERROR";
        client_os.write(errorMsg.getBytes());
        client_os.flush();
      } catch (Exception ex) {
        System.out.println("[CC] Error when sending error message: " +
                           ex.getMessage());
      }
    } finally {
      // try to close client socket at last
      try {
        clientSocket.close();
      } catch (Exception e) {
        System.out.println("[CC] Error when closing client socket: " +
                           e.getMessage());
      }
    }
    System.out.println("[CC] A client connection was ended!");
  }
}
