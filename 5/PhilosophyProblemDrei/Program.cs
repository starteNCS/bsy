using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace PhilosophyProblemDrei
{
  partial class Program
  {
    internal const int SLEEP_AMOUNT = 500;

    internal static readonly Mutex Mutex = new Mutex(false);

    static void Main(string[] args)
    {
      List<Philosoph> philosophs = ComputePhilosophersList();
      philosophs.ForEach(philosoph =>
      {
        Thread thread = new Thread(() => Philosopher(philosoph));
        thread.Name = "PHILOSOPHER_" + philosoph.PersonNo;

        Log("Starting thread for philisopher {0}", philosoph.PersonNo);
        thread.Start();
      });
    }

    private static List<Philosoph> ComputePhilosophersList()
    {
      Philosoph p1 = new Philosoph(1);
      Philosoph p2 = new Philosoph(2);
      Philosoph p3 = new Philosoph(3);
      Philosoph p4 = new Philosoph(4);
      Philosoph p5 = new Philosoph(5);
      Philosoph p6 = new Philosoph(6);

      p1.SetNeighbors(p2, p4, p3);
      p2.SetNeighbors(null, p1, null);
      p3.SetNeighbors(p6, p5, p1);
      p4.SetNeighbors(p1, null, null);
      p5.SetNeighbors(p3, null, null);
      p6.SetNeighbors(null, p3, null);

      return new[] { p1, p2, p3, p4, p5, p6 }.ToList();
    }

    internal static void Log(string msg, params object[] args)
    {
      msg = string.Format(msg, args);
      Console.WriteLine($"[{DateTime.Now:s}] - {msg}");
    }

    static void Philosopher(Philosoph philosoph)
    {
      while (true)
      {
        philosoph.Think();
        philosoph.TakeForks();
        philosoph.Eat();
        philosoph.PutForks();
      }
    }
  }
}