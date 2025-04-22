// javac AtomicUpdates.java && jar cvfe AtomicUpdates.jar AtomicUpdates AtomicUpdates.class 'AtomicUpdates$Buckets.class' && java -jar AtomicUpdates.jar

// https://rosettacode.org/wiki/Atomic_updates#Java

/* Define a data type consisting of a fixed number of 'buckets', each
 * containing a nonnegative integer value, which supports operations to:
 * - get the current value of any bucket
 * - remove a specified amount from one specified bucket and add it to
 *   another, preserving the total of all bucket values, and clamping
 *   the transferred amount to ensure the values remain non-negative
 * In order to exercise this data type, create one set of buckets, and
 * start three concurrent tasks:
 * - As often as possible, pick two buckets and make their values closer
 *   to equal.
 * - As often as possible, pick two buckets and arbitrarily redistribute
 *   their values.
 * - At whatever rate is convenient, display (by any means) the total
 *   value and, optionally, the individual values of each bucket.
 * The display task need not be explicit; use of e.g. a debugger or
 * trace tool is acceptable provided it is simple to set up to provide
 * the display.
 * This task is intended as an exercise in atomic operations. The sum of
 * the bucket values must be preserved even if the two tasks attempt to
 * perform transfers simultaneously, and a straightforward solution is
 * to ensure that at any time, only one transfer is actually occurring —
 * that the transfer operation is atomic.
 */

import java.util.Arrays;
import java.util.concurrent.ThreadLocalRandom;

public class AtomicUpdates {

    private static final int NUM_BUCKETS = 10;

    public static class Buckets {
        private final int[] data;

        public Buckets(int[] data) {
            this.data = data.clone();
        }

        public int getBucket(int index) {
            synchronized (data) {
                return data[index];
            }
        }

        public int transfer(int srcIndex, int dstIndex, int amount) {
            if (amount < 0)
                throw new IllegalArgumentException("negative amount: " + amount);
            if (amount == 0)
                return 0;

            synchronized (data) {
                if (data[srcIndex] - amount < 0)
                    amount = data[srcIndex];
                if (data[dstIndex] + amount < 0)
                    amount = Integer.MAX_VALUE - data[dstIndex];
                if (amount < 0)
                    throw new IllegalStateException();
                data[srcIndex] -= amount;
                data[dstIndex] += amount;
                return amount;
            }
        }

        public int[] getBuckets() {
            synchronized (data) {
                return data.clone();
            }
        }
    }

    private static long getTotal(int[] values) {
        long total = 0;
        for (int value : values) {
            total += value;
        }
        return total;
    }

    public static void main(String[] args) {
        ThreadLocalRandom rnd = ThreadLocalRandom.current();

        int[] values = new int[NUM_BUCKETS];
        for (int i = 0; i < values.length; i++)
            values[i] = rnd.nextInt() & Integer.MAX_VALUE;
        System.out.println("Initial Array: " + getTotal(values) + " " + Arrays.toString(values));

        Buckets buckets = new Buckets(values);
        new Thread(() -> equalize(buckets), "equalizer").start();
        new Thread(() -> transferRandomAmount(buckets), "transferrer").start();
        new Thread(() -> print(buckets), "printer").start();
    }

    private static void transferRandomAmount(Buckets buckets) {
        ThreadLocalRandom rnd = ThreadLocalRandom.current();
        while (true) {
            int srcIndex = rnd.nextInt(NUM_BUCKETS);
            int dstIndex = rnd.nextInt(NUM_BUCKETS);
            int amount = rnd.nextInt() & Integer.MAX_VALUE;
            buckets.transfer(srcIndex, dstIndex, amount);
        }
    }

    private static void equalize(Buckets buckets) {
        ThreadLocalRandom rnd = ThreadLocalRandom.current();
        while (true) {
            int srcIndex = rnd.nextInt(NUM_BUCKETS);
            int dstIndex = rnd.nextInt(NUM_BUCKETS);
            int amount = (buckets.getBucket(srcIndex) - buckets.getBucket(dstIndex)) / 2;
            if (amount >= 0)
                buckets.transfer(srcIndex, dstIndex, amount);
        }
    }

    private static void print(Buckets buckets) {
        while (true) {
            long nextPrintTime = System.currentTimeMillis() + 3000;
            long now;
            while ((now = System.currentTimeMillis()) < nextPrintTime) {
                try {
                    Thread.sleep(nextPrintTime - now);
                } catch (InterruptedException e) {
                    return;
                }
            }

            int[] bucketValues = buckets.getBuckets();
            System.out.println("Current values: " + getTotal(bucketValues) + " " + Arrays.toString(bucketValues));
        }
    }
}
