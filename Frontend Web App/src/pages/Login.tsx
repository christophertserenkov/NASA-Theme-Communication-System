import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { LogIn } from 'lucide-react';
import { Loader2 } from 'lucide-react';
import supabase from '@/helper/supabaseClient';

const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password,
        });
        if (error) {
            console.error('Error logging in:', error.message);
            setErrorMessage(error.message);
            setEmail('');
            setPassword('');
            setLoading(false);
        } else if (data) {
            navigate('/');
        }
    };

    return (
        <div className="w-full flex flex-col items-center mt-8">
            <h1 className="text-3xl font-semibold">Log In</h1>
            <form
                className="w-1/4 flex flex-col items-center mt-8 gap-4"
                onSubmit={handleLogin}
            >
                <Input
                    placeholder="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <Input
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <Button type="submit" disabled={loading}>
                    {loading ? (
                        <>
                            <Loader2 className="animate-spin" /> Please wait
                        </>
                    ) : (
                        <>
                            <LogIn /> Log in
                        </>
                    )}
                </Button>
            </form>
            {errorMessage && (
                <p className="mt-8 text-red-500">{errorMessage}</p>
            )}
        </div>
    );
};

export default Login;
