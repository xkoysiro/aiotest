from collections import deque
from datetime import datetime
import logging
from typing import Dict, List, Optional


class UserContextManager:
    def __init__(self, max_messages: int = 20):
        self.user_contexts: Dict[int, Dict] = {}
        self.max_messages = max_messages
        logging.info(f"✅ Менеджер контекста инициализирован (макс. сообщений: {max_messages})")

    def _ensure_user_context(self, user_id: int) -> Dict:
        """Создает контекст пользователя если не существует"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {
                'messages': deque(maxlen=self.max_messages),
                'created_at': datetime.now(),
                'last_activity': datetime.now(),
                'message_count': 0
            }
            logging.debug(f"🆕 Создан контекст для пользователя {user_id}")
        return self.user_contexts[user_id]

    def add_message(self, user_id: int, role: str, content: str) -> None:
        """Добавляет сообщение в контекст пользователя"""
        context = self._ensure_user_context(user_id)

        message = {
            'role': role,
            'content': content.strip(),
            'timestamp': datetime.now(),
            'message_id': context['message_count']
        }

        context['messages'].append(message)
        context['message_count'] += 1
        context['last_activity'] = datetime.now()

        logging.debug(f"📝 Добавлено сообщение {context['message_count']} для пользователя {user_id}, роль: {role}")

    def get_messages(self, user_id: int, include_system: bool = True) -> List[Dict]:
        """Возвращает все сообщения пользователя"""
        context = self._ensure_user_context(user_id)
        messages = list(context['messages'])

        if not include_system:
            messages = [msg for msg in messages if msg['role'] != 'system']

        return messages

    def get_formatted_messages(self, user_id: int) -> List[Dict[str, str]]:
        """Возвращает сообщения в формате для API"""
        messages = self.get_messages(user_id)
        return [{'role': msg['role'], 'content': msg['content']} for msg in messages]

    def clear_context(self, user_id: int) -> bool:
        """Очищает контекст пользователя"""
        if user_id in self.user_contexts:
            self.user_contexts[user_id]['messages'].clear()
            logging.info(f"🧹 Контекст пользователя {user_id} очищен")
            return True
        return False

    def get_context_stats(self, user_id: int) -> Optional[Dict]:
        """Возвращает статистику контекста"""
        if user_id in self.user_contexts:
            context = self.user_contexts[user_id]
            messages = list(context['messages'])

            user_msgs = len([m for m in messages if m['role'] == 'user'])
            assistant_msgs = len([m for m in messages if m['role'] == 'assistant'])
            system_msgs = len([m for m in messages if m['role'] == 'system'])

            return {
                'total_messages': len(messages),
                'user_messages': user_msgs,
                'assistant_messages': assistant_msgs,
                'system_messages': system_msgs,
                'created_at': context['created_at'],
                'last_activity': context['last_activity']
            }
        return None

    def prune_inactive_contexts(self, hours: int = 24) -> int:
        """Удаляет контексты неактивных пользователей"""
        now = datetime.now()
        pruned_count = 0

        for user_id in list(self.user_contexts.keys()):
            context = self.user_contexts[user_id]
            inactivity_hours = (now - context['last_activity']).total_seconds() / 3600

            if inactivity_hours > hours:
                del self.user_contexts[user_id]
                pruned_count += 1
                logging.info(f"🗑️ Удален контекст неактивного пользователя {user_id}")

        return pruned_count
