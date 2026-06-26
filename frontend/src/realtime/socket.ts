import { useStreamStore } from './streamStore';

const WS_URL = import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8000/ws";

class StreamingManager {
  private socket: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private isConnecting = false;
  private intentionalDisconnect = false;
  private heartbeatInterval: number | null = null;

  constructor() {
    this.url = `${WS_URL}/live`;
  }

  public connect() {
    if (this.socket?.readyState === WebSocket.OPEN || this.isConnecting) return;
    
    this.isConnecting = true;
    this.intentionalDisconnect = false;
    useStreamStore.getState().setConnectionStatus('connecting');
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("WebSocket connected to live data stream");
      this.reconnectAttempts = 0;
      this.isConnecting = false;
      useStreamStore.getState().setConnectionStatus('connected');
      this.startHeartbeat();
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleEvent(data.type, data.payload);
      } catch (e) {
        console.error("Failed to parse WebSocket message", e);
      }
    };

    this.socket.onclose = () => {
      console.warn("WebSocket disconnected");
      this.isConnecting = false;
      this.socket = null;
      useStreamStore.getState().setConnectionStatus('disconnected');
      this.stopHeartbeat();
      if (!this.intentionalDisconnect) {
        this.handleReconnect();
      }
    };

    this.socket.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.socket?.close();
    };
  }

  public disconnect() {
    if (this.socket) {
      this.intentionalDisconnect = true;
      this.isConnecting = false;
      this.socket.close();
      this.socket = null;
    }
  }

  private handleEvent(type: string, payload: any) {
    const store = useStreamStore.getState();
    
    switch (type) {
      case 'MISSION_STATE':
        store.setMissionState(payload);
        break;
      case 'TELEMETRY':
        store.updateTelemetry(payload);
        break;
      case 'PHYSICS':
        store.updatePhysics(payload);
        break;
      case 'FORECAST':
        store.updateForecast(payload);
        break;
      case 'DIGITAL_TWIN':
        store.updateDigitalTwin(payload);
        break;
      case 'SYSTEM':
        store.updateSystem(payload);
        break;
      case 'ALERTS':
        store.addAlert(payload);
        break;
      default:
        console.warn("Unknown event type received:", type);
    }
  }

  private handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      useStreamStore.getState().setConnectionStatus('reconnecting');
      const timeout = Math.min(1000 * Math.pow(1.5, this.reconnectAttempts), 10000);
      console.log(`Attempting to reconnect in ${timeout}ms... (Attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(), timeout);
    } else {
      console.error("Max WebSocket reconnect attempts reached.");
    }
  }

  private startHeartbeat() {
    this.stopHeartbeat();
    this.heartbeatInterval = window.setInterval(() => {
      if (this.socket?.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({ action: "ping" }));
      }
    }, 10000); // 10 seconds
  }

  private stopHeartbeat() {
    if (this.heartbeatInterval !== null) {
      window.clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  // API for React components to send commands to the backend (e.g. for replay engine)
  public sendCommand(action: string, payload: any = {}) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ action, ...payload }));
    } else {
      console.warn("Cannot send command, WebSocket is not open");
    }
  }
}

export const streamManager = new StreamingManager();
