using System;
using System.Linq;
using System.Threading;

namespace PhilosophyProblem
{
  partial class Program
  {
    private const int PHILIOSPHER_COUNT = 5;
    private const int SLEEP_AMOUNT = 500;

    private static PhilosopherState[] currentPhilisopherState = Enumerable.Repeat(PhilosopherState.THINKING, PHILIOSPHER_COUNT).ToArray();

    private static readonly Mutex mutex = new Mutex(false);

    private static Semaphore[] philosopherSemaphore = new Semaphore[PHILIOSPHER_COUNT];

    static void Main(string[] args)
    {
      for (int i = 0; i < PHILIOSPHER_COUNT; i++)
      {
        philosopherSemaphore[i] = new Semaphore(0, 2);
      }

      Enumerable.Range(0, PHILIOSPHER_COUNT).ToList().ForEach(philospher =>
      {
        Thread thread = new Thread(() => Philosopher(philospher));
        thread.Name = "PHILOSOPHER_" + philospher;

        Log("Starting thread for philisopher {0}", philospher);
        thread.Start();
      });
    }

    private static void Log(string msg, params object[] args)
    {
      msg = string.Format(msg, args);
      Console.WriteLine($"[{DateTime.Now:s}] - {msg}");
    }

    static void Philosopher(int philosoph)
    {
      while (true)
      {
        Log("Philosph {0} is thinking", philosoph);
        Think();
        Log("Philosph {0} is taking forks", philosoph);
        TakeForks(philosoph);
        Log("Philosph {0} is eating", philosoph);
        Eat();
        Log("Philosph {0} is putting forks", philosoph);
        PutForks(philosoph);
      }
    }

    static void Eat()
    {
      Thread.Sleep(SLEEP_AMOUNT);
    }

    static void Think()
    {
      Thread.Sleep(SLEEP_AMOUNT);
    }

    static void TakeForks(int philosoph)
    {
      mutex.WaitOne();
      currentPhilisopherState[philosoph] = PhilosopherState.HUNGRY;
      Test(philosoph);
      mutex.ReleaseMutex();
      philosopherSemaphore[philosoph].WaitOne();
    }

    static void PutForks(int philosoph)
    {
      mutex.WaitOne();
      currentPhilisopherState[philosoph] = PhilosopherState.THINKING;
      Test(Left(philosoph));
      Test(Right(philosoph));
      mutex.ReleaseMutex();
    }

    static void Test(int philisoph)
    {
      if (currentPhilisopherState[philisoph] == PhilosopherState.HUNGRY
          && currentPhilisopherState[Left(philisoph)] != PhilosopherState.EATING
          && currentPhilisopherState[Right(philisoph)] != PhilosopherState.EATING)
      {
        currentPhilisopherState[philisoph] = PhilosopherState.EATING;
        philosopherSemaphore[philisoph].Release();
      }
    }

    static int Left(int philisoph)
    {
      return (philisoph + PHILIOSPHER_COUNT - 1) % PHILIOSPHER_COUNT;
    }

    static int Right(int philosoph)
    {
      return (philosoph + 1) % PHILIOSPHER_COUNT;
    }
  }
}
