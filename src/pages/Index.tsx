import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import Icon from '@/components/ui/icon';
import { useToast } from '@/hooks/use-toast';

const ADMIN_EMAIL = 'suradaniil74@gmail.com';
const AUTH_URL = 'https://functions.poehali.dev/39c3bcf3-ff05-43e6-9752-8d71cb3f2726';
const ADMIN_URL = 'https://functions.poehali.dev/aa011f22-c7a0-4b11-b36e-e89178ddec31';
const GENERATE_URL = 'https://functions.poehali.dev/a4d631a0-21c0-4343-ad03-17b86f32820d';

interface User {
  id: number;
  email: string;
  energy_balance: number;
  is_admin: boolean;
}

const Index = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState<User[]>([]);
  const [sitePrompt, setSitePrompt] = useState('');
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  useEffect(() => {
    if (user?.is_admin) {
      loadUsers();
    }
  }, [user]);

  const loadUsers = async () => {
    try {
      const response = await fetch(ADMIN_URL, {
        headers: {
          'X-Admin-Email': user?.email || ''
        }
      });
      const data = await response.json();
      if (data.users) {
        setUsers(data.users);
      }
    } catch (error) {
      console.error('Failed to load users:', error);
    }
  };

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(AUTH_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: isLogin ? 'login' : 'register',
          email,
          password
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setUser(data.user);
        localStorage.setItem('user', JSON.stringify(data.user));
        toast({
          title: isLogin ? 'Вход выполнен' : 'Регистрация успешна',
          description: `Добро пожаловать! Ваш баланс: ${data.user.energy_balance} энергии`
        });
        setEmail('');
        setPassword('');
      } else {
        toast({
          title: 'Ошибка',
          description: data.error || 'Что-то пошло не так',
          variant: 'destructive'
        });
      }
    } catch (error) {
      toast({
        title: 'Ошибка',
        description: 'Не удалось подключиться к серверу',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const updateBalance = async (userId: number, newBalance: number) => {
    try {
      const response = await fetch(ADMIN_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Email': user?.email || ''
        },
        body: JSON.stringify({
          action: 'update_balance',
          user_id: userId,
          new_balance: newBalance
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        toast({
          title: 'Баланс обновлён',
          description: `Новый баланс: ${newBalance} энергии`
        });
        loadUsers();
        
        if (user && user.id === userId) {
          const updatedUser = { ...user, energy_balance: newBalance };
          setUser(updatedUser);
          localStorage.setItem('user', JSON.stringify(updatedUser));
        }
      } else {
        toast({
          title: 'Ошибка',
          description: data.error || 'Не удалось обновить баланс',
          variant: 'destructive'
        });
      }
    } catch (error) {
      toast({
        title: 'Ошибка',
        description: 'Не удалось подключиться к серверу',
        variant: 'destructive'
      });
    }
  };

  const generateSite = async () => {
    if (!sitePrompt.trim()) {
      toast({
        title: 'Ошибка',
        description: 'Введите описание сайта',
        variant: 'destructive'
      });
      return;
    }

    setIsGenerating(true);

    try {
      const response = await fetch(GENERATE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user?.id,
          prompt: sitePrompt
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setGeneratedHtml(data.html);
        const updatedUser = { ...user!, energy_balance: data.energy_remaining };
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
        toast({
          title: 'Сайт создан!',
          description: `Использовано ${data.energy_used} энергии. Осталось: ${data.energy_remaining}`
        });
      } else {
        toast({
          title: 'Ошибка',
          description: data.error || 'Не удалось создать сайт',
          variant: 'destructive'
        });
      }
    } catch (error) {
      toast({
        title: 'Ошибка',
        description: 'Не удалось подключиться к серверу',
        variant: 'destructive'
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    toast({
      title: 'Выход выполнен',
      description: 'До скорой встречи!'
    });
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 animate-gradient bg-[length:400%_400%] flex items-center justify-center p-4">
        <Card className="w-full max-w-6xl p-8 backdrop-blur-sm bg-white/95 animate-scale-in">
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-6 animate-fade-in">
              <div className="space-y-2">
                <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  POEHALI.DEV
                </h1>
                <p className="text-xl text-gray-600">100% бесплатная версия</p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
                  <Icon name="Zap" className="text-blue-600" size={24} />
                  <div>
                    <h3 className="font-semibold">Бесплатная энергия</h3>
                    <p className="text-sm text-gray-600">100 единиц при регистрации</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
                  <Icon name="Code" className="text-purple-600" size={24} />
                  <div>
                    <h3 className="font-semibold">Полный доступ</h3>
                    <p className="text-sm text-gray-600">Все функции платформы</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-4 bg-pink-50 rounded-lg hover:bg-pink-100 transition-colors">
                  <Icon name="Rocket" className="text-pink-600" size={24} />
                  <div>
                    <h3 className="font-semibold">Быстрый старт</h3>
                    <p className="text-sm text-gray-600">Создавайте проекты за минуты</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-4 animate-fade-in">
              <div className="flex gap-2 mb-4">
                <Button
                  variant={isLogin ? 'default' : 'outline'}
                  onClick={() => setIsLogin(true)}
                  className="flex-1"
                >
                  Вход
                </Button>
                <Button
                  variant={!isLogin ? 'default' : 'outline'}
                  onClick={() => setIsLogin(false)}
                  className="flex-1"
                >
                  Регистрация
                </Button>
              </div>

              <form onSubmit={handleAuth} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@email.com"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Пароль</Label>
                  <Input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                  disabled={loading}
                >
                  {loading ? 'Загрузка...' : isLogin ? 'Войти' : 'Зарегистрироваться'}
                </Button>
              </form>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            POEHALI.DEV
          </h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-blue-50 px-4 py-2 rounded-lg">
              <Icon name="Zap" className="text-blue-600" size={20} />
              <span className="font-semibold">{user.energy_balance}</span>
              <span className="text-sm text-gray-600">энергии</span>
            </div>
            <Button variant="outline" onClick={logout}>
              Выход
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        <section className="space-y-6 animate-fade-in">
          <div className="text-center space-y-2">
            <h2 className="text-4xl font-bold">Создайте свой сайт за минуту</h2>
            <p className="text-xl text-gray-600">
              Опишите, что хотите создать — нейросеть всё сделает
            </p>
          </div>

          <Card className="p-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="prompt">Что создаём?</Label>
                <Textarea
                  id="prompt"
                  value={sitePrompt}
                  onChange={(e) => setSitePrompt(e.target.value)}
                  placeholder="Например: Landing для кофейни с меню и формой заказа. Современный дизайн с градиентами."
                  className="text-lg min-h-24"
                  rows={3}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  <Icon name="Zap" className="inline text-blue-600" size={16} />
                  {' '}Стоимость: 20 энергии за запрос
                </div>
                <Button
                  onClick={generateSite}
                  disabled={isGenerating || user.energy_balance < 20}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                >
                  {isGenerating ? (
                    <>
                      <Icon name="Loader2" className="animate-spin mr-2" size={20} />
                      Создаём сайт...
                    </>
                  ) : (
                    <>
                      <Icon name="Sparkles" className="mr-2" size={20} />
                      Создать сайт
                    </>
                  )}
                </Button>
              </div>
            </div>
          </Card>

          {generatedHtml && (
            <Card className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold flex items-center gap-2">
                  <Icon name="Check" className="text-green-600" size={24} />
                  Ваш сайт готов!
                </h3>
                <Button
                  variant="outline"
                  onClick={() => {
                    const blob = new Blob([generatedHtml], { type: 'text/html' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'site.html';
                    a.click();
                  }}
                >
                  <Icon name="Download" size={16} className="mr-2" />
                  Скачать HTML
                </Button>
              </div>
              
              <div className="border rounded-lg overflow-hidden">
                <iframe
                  srcDoc={generatedHtml}
                  className="w-full h-96 border-0"
                  title="Generated Site Preview"
                />
              </div>
            </Card>
          )}
        </section>

        <section className="grid md:grid-cols-3 gap-6 animate-fade-in">
          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="space-y-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Icon name="Wand2" className="text-blue-600" size={24} />
              </div>
              <h3 className="text-xl font-semibold">ИИ генерация</h3>
              <p className="text-gray-600">
                Мощная нейросеть создаёт сайты по вашему описанию
              </p>
            </div>
          </Card>

          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="space-y-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Icon name="Zap" className="text-purple-600" size={24} />
              </div>
              <h3 className="text-xl font-semibold">Быстро и просто</h3>
              <p className="text-gray-600">
                От идеи до готового сайта за 30 секунд
              </p>
            </div>
          </Card>

          <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="space-y-4">
              <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center">
                <Icon name="Download" className="text-pink-600" size={24} />
              </div>
              <h3 className="text-xl font-semibold">Готовый код</h3>
              <p className="text-gray-600">
                Скачивайте HTML файл и размещайте где угодно
              </p>
            </div>
          </Card>
        </section>

        {user.is_admin && (
          <section className="space-y-6 animate-fade-in">
            <div className="flex items-center gap-2">
              <Icon name="Shield" className="text-purple-600" size={24} />
              <h2 className="text-3xl font-bold">Админ-панель</h2>
            </div>

            <div className="grid gap-4">
              {users.map((u) => (
                <Card key={u.id} className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <p className="font-semibold">{u.email}</p>
                        {u.is_admin && (
                          <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                            Админ
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600">ID: {u.id}</p>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <Icon name="Zap" className="text-blue-600" size={20} />
                        <span className="font-semibold text-lg">{u.energy_balance}</span>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            const amount = prompt(
                              `Сколько энергии добавить для ${u.email}?`,
                              '100'
                            );
                            if (amount !== null) {
                              const newBalance = u.energy_balance + parseInt(amount);
                              updateBalance(u.id, newBalance);
                            }
                          }}
                        >
                          <Icon name="Plus" size={16} />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => {
                            const newBalance = prompt(
                              `Установить баланс для ${u.email}:`,
                              u.energy_balance.toString()
                            );
                            if (newBalance !== null) {
                              updateBalance(u.id, parseInt(newBalance));
                            }
                          }}
                        >
                          <Icon name="Edit" size={16} />
                        </Button>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default Index;