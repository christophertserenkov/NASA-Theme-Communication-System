import { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Send } from 'lucide-react';
import { Loader2 } from 'lucide-react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import supabase from '@/helper/supabaseClient';
import { Database } from '@/types/supabase';

type Message = Database['public']['Tables']['Messages']['Row'];

const Home = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        const fetchMessages = async () => {
            const { data, error } = await supabase.from('Messages').select('*');
            if (error) {
                setErrorMessage(error.message);
            } else {
                setMessages(data);
            }
        };
        fetchMessages();
        setRefresh(false);
    }, [refresh]);

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        const { error } = await supabase
            .from('Messages')
            .insert([
                { sender: 'JPL', recipient: 'Whatney', content: message },
            ]);
        if (error) {
            setErrorMessage(error.message);
        } else {
            setErrorMessage('');
            setRefresh(true);
        }

        setMessage('');
        setLoading(false);
    };

    return (
        <div className="w-full flex flex-col items-center mt-8">
            <h1 className="text-3xl font-semibold">
                NASA Communication Network
            </h1>
            <form
                className="w-1/3 flex items-center mt-8 gap-4"
                onSubmit={handleSendMessage}
            >
                <Input
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Message"
                    required
                />
                <Button type="submit" disabled={loading}>
                    {loading ? (
                        <>
                            <Loader2 className="animate-spin" /> Please wait
                        </>
                    ) : (
                        <>
                            <Send /> Send
                        </>
                    )}
                </Button>
            </form>
            {errorMessage && (
                <p className="mt-8 text-red-500">{errorMessage}</p>
            )}
            <div className="w-3/4 mt-8">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="text-left w-48">
                                Sender
                            </TableHead>
                            <TableHead>Message</TableHead>
                            <TableHead className="w-64">Time</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {messages.map((message) => (
                            <TableRow key={message.id}>
                                <TableCell className="font-medium">
                                    {message.sender}
                                </TableCell>
                                <TableCell className="max-w-72 pr-16 whitespace-pre-wrap break-words">
                                    {message.content}
                                </TableCell>
                                <TableCell>
                                    {new Date(message.sent_at).toLocaleString()}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
};

export default Home;
