import time

class Processo:
    def __init__(self, pid):
        self.pid = pid
        self.relogio = 0  # Inicializa relógio lógico em 0

    def evento_interno(self, descricao):
        # Regra 1: Incrementa antes de executar
        self.relogio += 1
        print(f"[{self.pid}] Evento Interno ('{descricao}'). Relógio atualizado para: {self.relogio}")

    def enviar_mensagem(self, destino_pid):
        # Regra 1: Incrementa antes de enviar
        self.relogio += 1
        print(f"[{self.pid}] ENVIANDO msg para {destino_pid}. Relógio: {self.relogio} | Timestamp enviado: {self.relogio}")
        # Retorna a mensagem contendo o timestamp (L_i)
        return {'msg': 'conteudo', 'timestamp': self.relogio}

    def receber_mensagem(self, pacote, remetente_pid):
        timestamp_recebido = pacote['timestamp']
        
        # Regra 2 (Recebimento): L_j = max(L_j, t)
        old_relogio = self.relogio
        self.relogio = max(self.relogio, timestamp_recebido)
        
        # Aplica a Regra 1: Incrementa L_j após o ajuste
        self.relogio += 1
        
        print(f"[{self.pid}] RECEBENDO msg de {remetente_pid} (Ts: {timestamp_recebido}). "
              f"Max({old_relogio}, {timestamp_recebido}) + 1 -> Novo Relógio: {self.relogio}")

def main():
    # Inicializando os 3 processos
    p1 = Processo("P1")
    p2 = Processo("P2")
    p3 = Processo("P3")

    print("--- INÍCIO DA SIMULAÇÃO (ALGORITMO DE LAMPORT) ---")

    # 1. P1: Evento interno.
    p1.evento_interno("Processamento local")

    # 2. P2: Envia mensagem para P3.
    msg_p2_to_p3 = p2.enviar_mensagem("P3")

    # 3. P3: Recebe mensagem de P2.
    p3.receber_mensagem(msg_p2_to_p3, "P2")

    # 4. P1: Envia mensagem para P2.
    msg_p1_to_p2 = p1.enviar_mensagem("P2")

    # 5. P3: Evento interno.
    p3.evento_interno("Calculando dados")

    # 6. P2: Recebe mensagem de P1.
    p2.receber_mensagem(msg_p1_to_p2, "P1")

    # 7. P2: Envia mensagem para P1.
    msg_p2_to_p1 = p2.enviar_mensagem("P1")

    # 8. P1: Recebe mensagem de P2.
    p1.receber_mensagem(msg_p2_to_p1, "P2")

    print("\n--- ESTADO FINAL DOS RELÓGIOS ---")
    print(f"P1: {p1.relogio}")
    print(f"P2: {p2.relogio}")
    print(f"P3: {p3.relogio}")

if __name__ == "__main__":
    main()