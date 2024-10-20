# Copyright (c) 2024 Guilherme Werner
# SPDX-License-Identifier: MIT

import pyshark
import pandas as pd
import matplotlib.pyplot as plt

max_packets = 1000
trace_files = ["bedrock-60s", "java-60s"]

metrics_dict = {
    "test_name": [],
    "total_packets": [],
    "average_packet_size_kb": [],
    "total_acks": [],
    "total_syns": [],
    "average_latency_ms": []
}

for trace_file in trace_files:
    capture = pyshark.FileCapture(f"./trace/{trace_file}.pcap", keep_packets=False)

    data = []
    packet_count = 0

    for packet in capture:
        if "IP" in packet:
            try:
                timestamp = float(packet.sniff_timestamp)
                # Tamanho do pacote em bytes
                packet_size = int(packet.length)

                if "TCP" in packet:
                    ack_flag = int(packet.tcp.flags_ack) if hasattr(packet.tcp, "flags_ack") else 0
                    syn_flag = int(packet.tcp.flags_syn) if hasattr(packet.tcp, "flags_syn") else 0
                else:
                    ack_flag = 0
                    syn_flag = 0

                data.append({
                    "timestamp": timestamp,
                    "packet_size": packet_size,
                    "ack_flag": ack_flag,
                    "syn_flag": syn_flag
                })

                packet_count += 1

                if packet_count >= max_packets:
                    break
            except AttributeError:
                continue

    df = pd.DataFrame(data)

    # Calcular a latência em segundos e converter para milissegundos
    df["latency"] = df["timestamp"].diff() * 1000

    total_packets = len(df)
    average_packet_size = df["packet_size"].mean()
    total_acks = df["ack_flag"].sum()
    total_syns = df["syn_flag"].sum()
    average_latency = df["latency"].mean()

    metrics_dict["test_name"].append(trace_file)
    metrics_dict["total_packets"].append(total_packets)
    metrics_dict["average_packet_size_kb"].append(average_packet_size)
    metrics_dict["total_acks"].append(total_acks)
    metrics_dict["total_syns"].append(total_syns)
    metrics_dict["average_latency_ms"].append(round(average_latency, 2))

    metrics_df = pd.DataFrame([{
        "total_packets": total_packets,
        "average_packet_size_kb": average_packet_size,
        "total_acks": total_acks,
        "total_syns": total_syns,
        "average_latency_ms": round(average_latency, 2)
    }])

    metrics_df.to_csv(f"./trace/{trace_file}.csv", index=False)

metrics_df_all = pd.DataFrame(metrics_dict)

test_labels = {"java-60s": "Java (TCP)", "bedrock-60s": "Bedrock (UDP)"}

# Gráfico do total de pacotes
total_packets_values = [96849, 348204]
plt.figure(figsize=(6.4, 4.8))
plt.bar(trace_files, total_packets_values)
plt.title("Total de Pacotes por Teste")
#plt.xlabel("Teste")
plt.ylabel("Total de Pacotes")
plt.xticks(ticks=range(len(test_labels)), labels=[test_labels[file] for file in trace_files], rotation=45)
plt.tight_layout()
plt.savefig("./trace/total_packets_comparison.png")
plt.close()

# Gráfico do tamanho médio dos pacotes
plt.figure(figsize=(12, 6))
metrics_df_all.plot(kind="bar", y="average_packet_size_kb", legend=False)
plt.title("Tamanho Médio dos Pacotes por Teste")
#plt.xlabel("Teste")
plt.ylabel("Tamanho Médio dos Pacotes (kB)")
plt.xticks(ticks=range(len(test_labels)), labels=[test_labels[file] for file in trace_files], rotation=45)
plt.tight_layout()
plt.savefig("./trace/average_packet_size_comparison.png")
plt.close()

# Gráfico da latência média
plt.figure(figsize=(12, 6))
metrics_df_all.plot(kind="bar", y="average_latency_ms", legend=False)
plt.title("Latência Média por Teste")
#plt.xlabel("Teste")
plt.ylabel("Latência Média (ms)")
plt.xticks(ticks=range(len(test_labels)), labels=[test_labels[file] for file in trace_files], rotation=45)
plt.tight_layout()
plt.savefig("./trace/average_latency_comparison.png")
plt.close()

# Gráfico de Pizza para TCP - Dados vs Controle
# Filtrar apenas pacotes TCP
tcp_df = df[df["ack_flag"] > 0]

# Calcular os pacotes de dados (não são ACKs)
data_packets = len(df) - tcp_df.shape[0]
control_packets = tcp_df.shape[0]  # Inclui ACKs, SYNs, etc.

# Proporções
sizes = [data_packets, control_packets]
labels = ['Dados', 'Controle']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
plt.title('Distribuição dos Pacotes TCP: Dados vs Controle')
plt.savefig("./trace/tcp_packet_distribution.png")
plt.close()

print("Métricas e gráficos comparativos salvos.")
