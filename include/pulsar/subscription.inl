template< class T >
inline subscription< T >::subscription( source< T >& p, position& h ) :
    source_( p ),
    head_( h ),
    tail_( h ),
    alive_( true )
{
}

template< class T >
inline size_t subscription< T >::available()
{
    // apply memory barrier to ensure all positions are correct
    std::atomic_thread_fence( std::memory_order::memory_order_acquire );

    // number of slots available is the difference between the head and tail
    // this ensure the subscription can never read past the head
    return head_ - tail_;
}

template< class T >
inline const T& subscription< T >::at( size_t i )
{
    return source_.queue_.at( tail_ + i );
}

template< class T >
inline size_t subscription< T >::commit( size_t n )
{
    // issue a memory barrier to ensure the queue is consistent
    // across threads then increment tail
    std::atomic_thread_fence( std::memory_order::memory_order_release );
    tail_ += n;
    return n;
}

template< class T >
inline subscription< T >& subscription< T >::subscribe()
{
    return source_.subscribe( tail_ );
}

template< class T >
inline void subscription< T >::cancel()
{
    alive_ = false;
}
