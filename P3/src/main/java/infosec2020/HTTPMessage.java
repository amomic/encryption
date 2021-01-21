package infosec2020;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;

/**
 *  Utility functions for handling HTTP messages (requests and responses).
 *  Very rudimentary request and response parsing. Only works for requests
 *  at the moment. Chunked encoding is also not supported in this basic
 *  implementation.
 *  */
public class HTTPMessage {
  private int contentLength;
  private String host;
  private String method;
  private byte[] msgBuffer;
  private int port;
  private String startLine;

  private static final int DEFAULT_PORT = 80;
  private static final int BUFFER_SIZE = 1024;

  HTTPMessage() {
    startLine = "";
    method = "";
    host = "";
    port = 0;
  }

  /* used to read http requests. only works for GET requests. Return true if
     parsing was successful. Throws exception if there is an error. Returns
     false if only a CRLF is received. */
  public boolean parseRequest(InputStream is) throws Exception {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    int character;
    boolean startLineParsed = false;
    String streamLine = "";

    // parse request header
    while ((character = is.read()) != -1) {
      baos.write((byte)character);
      streamLine += (char)character;

      if (streamLine.endsWith("\n")) {
        streamLine = streamLine.replace("\r\n", "");

        // if empty line (end of header is reached): end header parsing
        if (streamLine.isEmpty())
          break;

        // parse request line
        if (!startLineParsed) {
          startLineParsed = true;
          startLine = streamLine;

          String[] startLineSplit = startLine.split(" ");
          if (startLineSplit.length < 3)
            throw new Exception("faulty Request-Line ");

          method = startLineSplit[0];
        }
        // parse host header field and set host and port variables accordingly
        else if (streamLine.toLowerCase().contains("host")) {
          String hostHeaderValue = streamLine.split(" ")[1];
          String[] hostLineSplit = hostHeaderValue.split(":");

          // check if a port is specified, else use default port
          if (hostLineSplit.length > 1) {
            host = hostLineSplit[0];
            port = Integer.parseInt(hostLineSplit[1]);
          } else {
            host = hostHeaderValue;
            port = DEFAULT_PORT;
          }
        }

        streamLine = "";
      }
    }

    if (startLine.equals("")) {
      return false;
    }

    if (character == -1)
      throw new Exception("connection - was closed!");

    if (host == null)
      throw new Exception("no host header field");

    System.out.println("[HM] New request... Host: " + host + ":" + port +
                       " - Request-Line: " + startLine);
    msgBuffer = baos.toByteArray();
    return true;
  }

  /* returns the response bytes */
  public byte[] getMsgBuffer() { return msgBuffer; }

  /* returns the host a request is send to */
  public String getHost() { return host; }

  /* returns the port a request is send to */
  public int getPort() { return port; }
}
