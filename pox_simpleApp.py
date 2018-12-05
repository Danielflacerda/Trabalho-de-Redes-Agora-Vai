#coding=UTF-8
# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger()

def _handle_PacketIn (event):

  #Criação da mensagem a ser enviada.
  msg = of.ofp_flow_mod()

  #Obtém o ip destino do evento.
  dstip = event.parsed.find("ipv4").dstip

  #Definição padrão dos atributos da mensagem a ser enviada.
  msg.match.dl_type = 0x800    
  msg.match.nw_dst = dstip  
  
  #Log do evento para demonstração.
  print("Switch: " + str(event.dpid))
  print("Event to " + str(dstip))

  #Definindo a porta destino para os eventos relacionados ao switch 1.
  if event.dpid == 1:
    if dstip == "10.10.2.101" or  dstip == "10.10.2.102" or  dstip == "10.10.2.103":
      msg.actions.append(of.ofp_action_output(port = 1))
    elif dstip == "10.10.3.101" or  dstip == "10.10.3.102" or  dstip == "10.10.3.103":
      msg.actions.append(of.ofp_action_output(port = 2))
    elif dstip == "10.10.1.101":
      msg.actions.append(of.ofp_action_output(port = 3))
    elif dstip == "10.10.1.102":
      msg.actions.append(of.ofp_action_output(port = 4))
    elif dstip == "10.10.1.103":
      msg.actions.append(of.ofp_action_output(port = 5))

  #Definindo a porta destino para os eventos relacionados ao switch 2.
  elif event.dpid == 2:
    if dstip == "10.10.1.101" or  dstip == "10.10.1.102" or  dstip == "10.10.1.103":
      msg.actions.append(of.ofp_action_output(port = 1))
    elif dstip == "10.10.3.101" or  dstip == "10.10.3.102" or  dstip == "10.10.3.103":
      msg.actions.append(of.ofp_action_output(port = 2))
    elif dstip == "10.10.2.101":
      msg.actions.append(of.ofp_action_output(port = 3))
    elif dstip == "10.10.2.102":
      msg.actions.append(of.ofp_action_output(port = 4))
    elif dstip == "10.10.2.103":
      msg.actions.append(of.ofp_action_output(port = 5))

  #Definindo a porta destino para os eventos relacionados ao switch 3.
  elif event.dpid == 3:
    if dstip == "10.10.2.101" or  dstip == "10.10.2.102" or  dstip == "10.10.2.103":
      msg.actions.append(of.ofp_action_output(port = 1))
    elif dstip == "10.10.1.101" or  dstip == "10.10.1.102" or  dstip == "10.10.1.103":
      msg.actions.append(of.ofp_action_output(port = 2))
    elif dstip == "10.10.3.101":
      msg.actions.append(of.ofp_action_output(port = 3))
    elif dstip == "10.10.3.102":
      msg.actions.append(of.ofp_action_output(port = 4))
    elif dstip == "10.10.3.103":
      msg.actions.append(of.ofp_action_output(port = 5))
  
  #Envio da mensagem.
  event.connection.send(msg)

  #Tratamento de perda de pacote
  msg = of.ofp_packet_out()
  msg.data = event.ofp
  msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
  event.connection.send(msg)

def launch (reactive = False):
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)